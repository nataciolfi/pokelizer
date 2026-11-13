"""SQLite connections and explicit, atomic, checksum-verified schema upgrades."""

from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import sqlite3

import click
from flask import current_app, g

MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"


def connect_database(database: str | Path) -> sqlite3.Connection:
    """Every application connection enables and verifies foreign-key enforcement."""
    connection = sqlite3.connect(str(database), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA recursive_triggers = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        connection.close()
        raise RuntimeError("SQLite não ativou a verificação de chaves estrangeiras.")
    return connection


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database = current_app.config["DATABASE"]
        if database != ":memory:":
            Path(database).parent.mkdir(parents=True, exist_ok=True)
        g.db = connect_database(database)
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        # sqlite3.close rolls back any uncommitted transaction.
        connection.close()


@contextmanager
def transaction(connection: sqlite3.Connection):
    """Compose transactions with savepoints; never commit another caller's work."""
    if connection.in_transaction:
        name = "nested_" + __import__("uuid").uuid4().hex
        connection.execute(f"SAVEPOINT {name}")
        try:
            yield connection
            connection.execute(f"RELEASE SAVEPOINT {name}")
        except BaseException:
            connection.execute(f"ROLLBACK TO SAVEPOINT {name}")
            connection.execute(f"RELEASE SAVEPOINT {name}")
            raise
    else:
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise


def _statements(sql: str):
    """Use SQLite's own completeness parser, including multi-statement triggers."""
    statement = ""
    for line in sql.splitlines(keepends=True):
        statement += line
        if sqlite3.complete_statement(statement):
            yield statement
            statement = ""
    if statement.strip() and any(not line.lstrip().startswith("--") for line in statement.splitlines()):
        raise ValueError("Migração SQL incompleta.")


def upgrade(connection: sqlite3.Connection, migrations: Path = MIGRATIONS) -> list[int]:
    if sqlite3.sqlite_version_info < (3, 37, 0):
        raise RuntimeError("SQLite 3.37 ou superior é necessário para tabelas STRICT.")
    if connection.in_transaction:
        raise RuntimeError("Finalize a transação antes de atualizar o esquema.")
    # upgrade() is public and may receive a raw sqlite3 connection.
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA recursive_triggers = ON")
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise RuntimeError("Migração exige verificação de chaves estrangeiras ativa.")
    files = sorted(migrations.glob("[0-9][0-9][0-9]_*.sql"))
    if not files:
        raise RuntimeError("Nenhuma migração encontrada.")
    versions = [int(path.name.split("_", 1)[0]) for path in files]
    if versions != list(range(1, len(files) + 1)):
        raise RuntimeError("Migrações devem ser consecutivas e começar em 001.")
    applied = []
    with transaction(connection):
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
        if tables and "SCHEMA_MIGRATION" not in tables:
            raise RuntimeError(
                "Banco legado sem versão: não foi alterado. Faça backup; use db-import-legacy "
                "para validar uma cópia em outro arquivo. Consulte backend/README.md."
            )
        connection.execute("""CREATE TABLE IF NOT EXISTS SCHEMA_MIGRATION (
            version INTEGER PRIMARY KEY, filename TEXT NOT NULL UNIQUE,
            checksum TEXT NOT NULL, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) STRICT""")
        history = {row["version"]: row for row in connection.execute("SELECT * FROM SCHEMA_MIGRATION")}
        if sorted(history) != list(range(1, len(history) + 1)) or set(history) - set(versions):
            raise RuntimeError("Histórico de migrações incompatível com esta versão do código.")
        for version, path in zip(versions, files):
            content = path.read_text(encoding="utf-8")
            checksum = sha256(content.encode("utf-8")).hexdigest()
            if version in history:
                if history[version]["checksum"] != checksum or history[version]["filename"] != path.name:
                    raise RuntimeError(f"Migração já aplicada foi modificada: {path.name}")
                continue
            for statement in _statements(content):
                # Foreign keys must stay enabled; migration files contain DDL, not transaction control.
                normalized = " ".join(statement.upper().split())
                if "PRAGMA FOREIGN_KEYS" in normalized:
                    continue
                connection.execute(statement)
            connection.execute("INSERT INTO SCHEMA_MIGRATION(version,filename,checksum) VALUES (?,?,?)", (version, path.name, checksum))
            applied.append(version)
        if connection.execute("PRAGMA foreign_key_check").fetchone():
            raise RuntimeError("Atualização violou chaves estrangeiras; transação revertida.")
    return applied


def init_db(app) -> None:
    """Explicit initialization/upgrade entry point, never called by application startup."""
    with app.app_context():
        upgrade(get_db())


def backup_database(connection: sqlite3.Connection, destination: Path) -> None:
    if connection.in_transaction:
        raise RuntimeError("Finalize a transação antes de gerar o backup.")
    # Exclusive file creation prevents accidentally overwriting an existing backup.
    with destination.open("xb"):
        pass
    try:
        with sqlite3.connect(destination) as backup:
            connection.backup(backup)
    except BaseException:
        destination.unlink(missing_ok=True)
        raise


def import_legacy(source: Path, destination: Path) -> None:
    """Validate an unversioned database into a NEW file; source remains byte-for-byte intact.

    No domain facts or mechanics are inferred. If stricter integrity rejects any row,
    the destination is removed and the entire source remains available for curation.
    """
    if source.resolve() == destination.resolve() or destination.exists():
        raise ValueError("O destino deve ser um arquivo novo, diferente da origem.")
    if not source.is_file():
        raise ValueError("Banco de origem inexistente.")
    original = sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)
    original.row_factory = sqlite3.Row
    original.execute("BEGIN")  # Consistent read snapshot even if another process writes.
    try:
        with destination.open("xb"):
            pass
    except BaseException:
        original.close()
        raise
    target = None
    try:
        target = connect_database(destination)
        upgrade(target)
        legacy_tables = [row[0] for row in original.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        supported = ["USUARIO", "ESPECIE", "FORMA", "JOGO", "DADOS_FORMA_JOGO", "TIPO", "TIPO_FORMA_JOGO", "HABILIDADE", "HABILIDADE_FORMA_JOGO", "METODO_OBTENCAO", "METODO_FORMA_JOGO", "NATUREZA", "POKEMON_COLECAO"]
        if set(legacy_tables) - set(supported):
            raise ValueError("A origem contém tabelas não reconhecidas; exporte e revise antes de importar.")
        with transaction(target):
            target.execute("PRAGMA defer_foreign_keys = ON")
            for table in supported:
                if table not in legacy_tables:
                    continue
                columns = [row["name"] for row in original.execute(f'PRAGMA table_info("{table}")')]
                allowed = {row["name"] for row in target.execute(f'PRAGMA table_info("{table}")')}
                if set(columns) - allowed:
                    raise ValueError(f"Colunas legadas sem mapeamento em {table}; origem preservada.")
                names = ",".join('"' + column.replace('"', '""') + '"' for column in columns)
                for row in original.execute(f'SELECT * FROM "{table}"'):
                    try:
                        target.execute(f'INSERT INTO "{table}" ({names}) VALUES ({",".join("?" for _ in columns)})', tuple(row))
                    except sqlite3.IntegrityError as exc:
                        raise ValueError(f"Revisão necessária em {table}, chave {row[0]}: {exc}. Nenhuma linha importada; origem intacta.") from exc
            if target.execute("PRAGMA foreign_key_check").fetchone():
                raise ValueError("A cópia contém referências inválidas; origem intacta.")
    except BaseException:
        if target is not None:
            target.close()
        destination.unlink(missing_ok=True)
        raise
    finally:
        original.close()
        if target is not None:
            target.close()


def register_cli(app) -> None:
    @app.cli.command("db-init")
    def db_init():
        """Initialize an empty database or apply pending migrations safely."""
        _upgrade_command()

    @app.cli.command("db-upgrade")
    def db_upgrade():
        """Apply only ordered, unapplied migrations without recreation."""
        _upgrade_command()

    def _upgrade_command():
        try:
            applied = upgrade(get_db())
        except (RuntimeError, ValueError, sqlite3.Error) as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(f"Migrações aplicadas: {applied or 'nenhuma (atualizado)'}")

    @app.cli.command("db-status")
    def db_status():
        """Read schema history without initializing the database."""
        try:
            for row in get_db().execute("SELECT version,filename,checksum FROM SCHEMA_MIGRATION ORDER BY version"):
                click.echo(f"{row['version']}: {row['filename']} {row['checksum']}")
        except sqlite3.OperationalError as exc:
            raise click.ClickException("Banco ainda não versionado; execute db-init em banco vazio.") from exc

    @app.cli.command("db-backup")
    @click.argument("destination", type=click.Path(path_type=Path))
    def db_backup(destination):
        """Write a consistent backup to a NEW file."""
        try:
            backup_database(get_db(), destination)
        except (OSError, RuntimeError, sqlite3.Error) as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(str(destination))

    @app.cli.command("db-import-legacy")
    @click.argument("source", type=click.Path(exists=True, path_type=Path))
    @click.argument("destination", type=click.Path(path_type=Path))
    def db_import_legacy(source, destination):
        """Validate legacy data into a new file, without changing the source."""
        try:
            import_legacy(source, destination)
        except (ValueError, RuntimeError, sqlite3.Error, OSError) as exc:
            raise click.ClickException(str(exc)) from exc
        click.echo(f"Cópia validada: {destination}. Revise antes de configurar DATABASE.")
