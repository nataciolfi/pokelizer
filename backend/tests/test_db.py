"""Connection lifecycle, non-destructive upgrades and legacy preservation."""

from hashlib import sha256
from pathlib import Path
import sqlite3

import pytest
from werkzeug.security import generate_password_hash

from pokeanalyzer import create_app
from pokeanalyzer.db import (backup_database, connect_database, get_db, import_legacy,
                             init_db, transaction, upgrade)


def test_clean_init_repeatable_upgrade_and_persistence(tmp_path):
    path = tmp_path / "catalog.sqlite3"
    db = connect_database(path)
    assert db.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert upgrade(db) == [1]
    with transaction(db):
        db.execute("INSERT INTO USUARIO(nome_usuario,email,senha_hash) VALUES (?,?,?)",
                   ("fixture_user", "fixture@example.invalid", generate_password_hash("password123")))
    assert upgrade(db) == []
    db.close()
    with connect_database(path) as reopened:
        assert reopened.execute("SELECT nome_usuario FROM USUARIO").fetchone()[0] == "fixture_user"
        assert reopened.execute("PRAGMA foreign_key_check").fetchall() == []


def test_migration_failure_rolls_back_whole_upgrade(tmp_path):
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "001_initial.sql").write_text("CREATE TABLE fixture(id INTEGER PRIMARY KEY) STRICT;\nINSERT INTO fixture VALUES(1);\n")
    db = connect_database(tmp_path / "rollback.sqlite3")
    upgrade(db, migrations)
    (migrations / "002_failure.sql").write_text("CREATE TABLE migration_marker(id INTEGER PRIMARY KEY) STRICT;\nINSERT INTO fixture VALUES(2);\nINSERT INTO fixture VALUES(1);\n")
    with pytest.raises(sqlite3.IntegrityError):
        upgrade(db, migrations)
    assert [row[0] for row in db.execute("SELECT id FROM fixture")] == [1]
    assert db.execute("SELECT COUNT(*) FROM SCHEMA_MIGRATION").fetchone()[0] == 1
    assert db.execute("SELECT name FROM sqlite_master WHERE name='migration_marker'").fetchone() is None
    db.close()


def test_modified_migration_is_rejected(tmp_path):
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    file = migrations / "001_initial.sql"
    file.write_text("CREATE TABLE fixture(id INTEGER PRIMARY KEY) STRICT;\n")
    db = connect_database(":memory:")
    upgrade(db, migrations)
    file.write_text(file.read_text() + "-- changed\n")
    with pytest.raises(RuntimeError, match="modificada"):
        upgrade(db, migrations)
    db.close()


def test_nested_transaction_failure_preserves_outer_work(tmp_path):
    db = connect_database(":memory:")
    db.execute("CREATE TABLE fixture(id INTEGER PRIMARY KEY)")
    with transaction(db):
        db.execute("INSERT INTO fixture VALUES(1)")
        with pytest.raises(ValueError):
            with transaction(db):
                db.execute("INSERT INTO fixture VALUES(2)")
                raise ValueError("rollback nested")
        assert db.in_transaction
        db.execute("INSERT INTO fixture VALUES(3)")
    assert [row[0] for row in db.execute("SELECT id FROM fixture")] == [1, 3]
    db.close()


def test_flask_context_closes_and_rolls_back(tmp_path):
    path = tmp_path / "lifecycle.sqlite3"
    app = create_app({"TESTING": True, "DATABASE": str(path)})
    assert not path.exists(), "app startup must not silently initialize a database"
    init_db(app)
    with app.app_context():
        connection = get_db()
        assert connection is get_db()
        connection.execute("INSERT INTO ESPECIE(numero_nacional,nome_pt) VALUES(99999,'FIXTURE uncommitted')")
    with pytest.raises(sqlite3.ProgrammingError):
        connection.execute("SELECT 1")
    reopened = connect_database(path)
    assert reopened.execute("SELECT COUNT(*) FROM ESPECIE").fetchone()[0] == 0
    reopened.close()


def test_legacy_upgrade_preserves_source_and_identity(tmp_path):
    source = tmp_path / "old?#.sqlite3"
    original = sqlite3.connect(source)
    original.executescript((Path(__file__).parent / "fixtures" / "legacy_v0.sql").read_text())
    password_hash = generate_password_hash("fixture password")
    original.execute("INSERT INTO USUARIO(id_usuario,nome_usuario,email,senha_hash) VALUES (42,?,?,?)", ("legacy_fixture", "legacy@example.invalid", password_hash))
    original.execute("INSERT INTO ESPECIE(id_especie,numero_nacional,nome_pt) VALUES (17,99999,'FIXTURE legacy species')")
    original.execute("INSERT INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(9,17,'fixture','FIXTURE standard',1)")
    original.execute("INSERT INTO JOGO(id_jogo,nome) VALUES(8,'FIXTURE legacy game')")
    original.execute("INSERT INTO DADOS_FORMA_JOGO(id_dados_forma,id_forma,id_jogo,status_presenca,pode_ser_registrada,fonte_url,data_verificacao) VALUES(7,9,8,'nativa','sim','https://example.invalid/legacy','2026-11-13')")
    original.execute("INSERT INTO POKEMON_COLECAO(id_pokemon_colecao,id_usuario,id_dados_forma_atual,apelido) VALUES(91,42,7,'FIXTURE preserved specimen')")
    original.commit()
    original.close()
    before = sha256(source.read_bytes()).hexdigest()
    protected = connect_database(source)
    with pytest.raises(RuntimeError, match="legado"):
        upgrade(protected)
    protected.close()
    assert sha256(source.read_bytes()).hexdigest() == before
    destination = tmp_path / "upgraded.sqlite3"
    import_legacy(source, destination)
    assert sha256(source.read_bytes()).hexdigest() == before
    db = connect_database(destination)
    user = db.execute("SELECT * FROM USUARIO WHERE id_usuario=42").fetchone()
    assert user["senha_hash"] == password_hash
    assert db.execute("SELECT nome_pt FROM ESPECIE WHERE id_especie=17").fetchone()[0] == "FIXTURE legacy species"
    specimen = db.execute("SELECT pc.id_pokemon_colecao,pc.apelido,e.numero_nacional FROM POKEMON_COLECAO pc JOIN DADOS_FORMA_JOGO d ON d.id_dados_forma=pc.id_dados_forma_atual JOIN FORMA f ON f.id_forma=d.id_forma JOIN ESPECIE e ON e.id_especie=f.id_especie WHERE pc.id_usuario=42").fetchone()
    assert tuple(specimen) == (91, "FIXTURE preserved specimen", 99999)
    assert upgrade(db) == []
    db.close()
    with pytest.raises(ValueError, match="novo"):
        import_legacy(source, destination)


def test_legacy_rejection_leaves_original_and_no_partial_copy(tmp_path):
    source = tmp_path / "invalid.sqlite3"
    with sqlite3.connect(source) as db:
        db.executescript("CREATE TABLE USUARIO (id_usuario INTEGER PRIMARY KEY, nome_usuario TEXT, email TEXT, senha_hash TEXT); INSERT INTO USUARIO VALUES(1,'x','x','x');")
    before = source.read_bytes()
    destination = tmp_path / "rejected.sqlite3"
    with pytest.raises(ValueError, match="Revisão necessária"):
        import_legacy(source, destination)
    assert source.read_bytes() == before
    assert not destination.exists()


def test_consistent_backup_never_overwrites(tmp_path):
    db = connect_database(tmp_path / "original.sqlite3")
    upgrade(db)
    destination = tmp_path / "backup.sqlite3"
    backup_database(db, destination)
    before = destination.read_bytes()
    with pytest.raises(FileExistsError):
        backup_database(db, destination)
    assert destination.read_bytes() == before
    db.close()


def test_upgrade_enables_integrity_on_raw_sqlite_connection():
    raw = sqlite3.connect(":memory:")
    assert raw.execute("PRAGMA foreign_keys").fetchone()[0] == 0
    upgrade(raw)
    assert raw.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert raw.execute("PRAGMA recursive_triggers").fetchone()[0] == 1
    with pytest.raises(sqlite3.IntegrityError):
        raw.execute("INSERT INTO FORMA(id_especie,codigo_forma,nome_forma) VALUES(999,'fixture','FIXTURE orphan')")
    raw.close()


def test_successful_new_migration_preserves_existing_rows(tmp_path):
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "001_initial.sql").write_text("CREATE TABLE fixture(id INTEGER PRIMARY KEY, name TEXT NOT NULL) STRICT;\nINSERT INTO fixture VALUES(17,'preserved');\n")
    path = tmp_path / "versioned.sqlite3"
    db = connect_database(path)
    assert upgrade(db, migrations) == [1]
    (migrations / "002_add_notes.sql").write_text("ALTER TABLE fixture ADD COLUMN notes TEXT;\n")
    assert upgrade(db, migrations) == [2]
    db.close()
    db = connect_database(path)
    assert tuple(db.execute("SELECT id,name,notes FROM fixture").fetchone()) == (17, "preserved", None)
    assert [r[0] for r in db.execute("SELECT version FROM SCHEMA_MIGRATION ORDER BY version")] == [1, 2]
    assert upgrade(db, migrations) == []
    db.close()
