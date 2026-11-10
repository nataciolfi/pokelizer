"""Aplicação Flask do PokéAnalyzer."""

import os
from pathlib import Path

from flask import Flask

from .api import api
from .db import close_db, init_db


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("POKEANALYZER_SECRET_KEY", "dev-only-change-this-secret-key"),
        DATABASE=os.environ.get(
            "POKEANALYZER_DATABASE",
            str(Path(app.instance_path) / "pokelizer.sqlite3"),
        ),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("POKEANALYZER_COOKIE_SECURE", "0") == "1",
        MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    if os.environ.get("FLASK_ENV", "").lower() == "production" and app.config["SECRET_KEY"].startswith("dev-only"):
        raise RuntimeError("Configure POKEANALYZER_SECRET_KEY antes de executar em produção.")

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    app.register_blueprint(api, url_prefix="/api")
    init_db(app)
    return app
