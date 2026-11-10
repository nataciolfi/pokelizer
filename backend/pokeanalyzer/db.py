"""Gerenciamento de conexões SQLite por contexto de requisição Flask."""

import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database = current_app.config["DATABASE"]
        if database != ":memory:":
            Path(database).parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(database, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db(app) -> None:
    schema_path = Path(__file__).resolve().parents[1] / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")
    with app.app_context():
        connection = get_db()
        connection.executescript(schema)
        connection.commit()
