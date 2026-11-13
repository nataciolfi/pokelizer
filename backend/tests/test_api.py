"""Testes de integração da API usando um banco SQLite temporário."""

import pytest

from pokeanalyzer import create_app
from pokeanalyzer.db import get_db, init_db
from pathlib import Path


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.sqlite3"
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "DATABASE": str(database),
        "SESSION_COOKIE_SECURE": False,
    })
    init_db(app)
    with app.app_context():
        db = get_db()
        db.executescript((Path(__file__).parent / "fixtures" / "catalog.sql").read_text())
        db.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def get_csrf(client) -> str:
    response = client.get("/api/csrf")
    assert response.status_code == 200
    return response.get_json()["csrf_token"]


def create_user(client, nome="aluno_teste", email="aluno@example.com"):
    token = get_csrf(client)
    response = client.post(
        "/api/auth/cadastro",
        json={"nome_usuario": nome, "email": email, "senha": "senha-segura-123"},
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 201
    return response.get_json()


def test_status_and_catalog_search(client):
    assert client.get("/api/status").get_json()["status"] == "ok"
    response = client.get("/api/pokemon?busca=species")
    assert response.status_code == 200
    assert response.get_json()["total"] == 1
    assert response.get_json()["itens"][0]["tipos"] == ["FIXTURE type A"]


def test_register_and_private_collection_crud(client):
    create_user(client)
    token = get_csrf(client)

    added = client.post(
        "/api/colecao",
        json={
            "id_dados_forma_atual": 1,
            "id_metodo_obtencao": 1,
            "id_habilidade_forma": 1,
            "id_mecanica": 1,
            "apelido": "Faísca",
            "nivel": 25,
        },
        headers={"X-CSRF-Token": token},
    )
    assert added.status_code == 201
    pokemon_id = added.get_json()["id_pokemon_colecao"]

    listing = client.get("/api/colecao")
    assert listing.status_code == 200
    assert listing.get_json()["total"] == 1
    assert listing.get_json()["itens"][0]["apelido"] == "Faísca"

    deleted = client.delete(
        f"/api/colecao/{pokemon_id}", headers={"X-CSRF-Token": token}
    )
    assert deleted.status_code == 200
    assert client.get("/api/colecao").get_json()["total"] == 0


def test_collection_requires_login(client):
    assert client.get("/api/colecao").status_code == 401


def test_collection_is_isolated_between_users(client):
    first = create_user(client, "aluno_um", "um@example.com")
    token = first["csrf_token"]
    created = client.post(
        "/api/colecao",
        json={"id_dados_forma_atual": 1},
        headers={"X-CSRF-Token": token},
    )
    pokemon_id = created.get_json()["id_pokemon_colecao"]

    client.post("/api/auth/logout", headers={"X-CSRF-Token": get_csrf(client)})
    create_user(client, "aluno_dois", "dois@example.com")
    assert client.get(f"/api/colecao/{pokemon_id}").status_code == 404
    assert client.get("/api/colecao").get_json()["total"] == 0


def test_csrf_is_required(client):
    response = client.post(
        "/api/auth/cadastro",
        json={"nome_usuario": "aluno", "email": "a@example.com", "senha": "senha-segura-123"},
    )
    assert response.status_code == 403


def test_invalid_level_is_rejected(client):
    create_user(client)
    response = client.post(
        "/api/colecao",
        json={"id_dados_forma_atual": 1, "nivel": 101},
        headers={"X-CSRF-Token": get_csrf(client)},
    )
    assert response.status_code == 400


def test_incompatible_ability_is_rejected(client):
    create_user(client)
    response = client.post(
        "/api/colecao",
        json={"id_dados_forma_atual": 1, "id_habilidade_forma": 999},
        headers={"X-CSRF-Token": get_csrf(client)},
    )
    assert response.status_code == 400


def test_absent_form_cannot_be_added_to_collection(client, app):
    create_user(client)
    with app.app_context():
        db = get_db()
        db.execute("UPDATE DADOS_FORMA_JOGO SET status_presenca = 'ausente', pode_ser_registrada = 'nao' WHERE id_dados_forma = 1")
        db.commit()
    response = client.post(
        "/api/colecao",
        json={"id_dados_forma_atual": 1},
        headers={"X-CSRF-Token": get_csrf(client)},
    )
    assert response.status_code == 400


def test_login_after_logout(client):
    create_user(client, "login_user", "login@example.com")
    client.post("/api/auth/logout", headers={"X-CSRF-Token": get_csrf(client)})
    token = get_csrf(client)
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "senha": "senha-segura-123"},
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 200
    assert response.get_json()["usuario"]["email"] == "login@example.com"


def test_duplicate_email_is_rejected(client):
    create_user(client, "primeiro_usuario", "same@example.com")
    response = client.post(
        "/api/auth/cadastro",
        json={"nome_usuario": "segundo_usuario", "email": "same@example.com", "senha": "senha-segura-123"},
        headers={"X-CSRF-Token": get_csrf(client)},
    )
    assert response.status_code == 400


def test_global_catalog_without_game_data_and_filters(client, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO ESPECIE(numero_nacional,nome_pt,geracao_origem) VALUES(99902,'FIXTURE global only',2)")
        species = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO FORMA(id_especie,codigo_forma,nome_forma) VALUES(?,'global','FIXTURE no game')", (species,))
        db.commit()
    result = client.get("/api/pokemon?busca=99902").get_json()
    assert result["total"] == 1
    assert result["itens"][0]["id_dados_forma"] is None
    assert result["itens"][0]["tipos"] == []
    assert client.get("/api/pokemon?geracao=2").get_json()["total"] == 1
    assert client.get("/api/pokemon?jogo=1&tipo=1&geracao=1").get_json()["total"] == 1
    assert client.get("/api/pokemon?jogo=1&tipo=1&geracao=2").get_json()["total"] == 0
    assert client.get("/api/pokemon?tipo=1.2").status_code == 400
    assert client.get(f"/api/pokemon?tipo={2**63}").status_code == 400


@pytest.mark.parametrize("value", [True, 1.5, "1.0", "-1", 0, 2**63])
def test_specimen_integer_fields_do_not_coerce_invalid_json(client, value):
    create_user(client)
    response = client.post("/api/colecao", json={"id_dados_forma_atual": value},
        headers={"X-CSRF-Token": get_csrf(client)})
    assert response.status_code == 400


def test_acquisition_history_survives_transfer_context(client, app):
    create_user(client)
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO METODO_OBTENCAO(id_metodo,nome) VALUES(2,'FIXTURE original acquisition only')")
        db.commit()
    response = client.post("/api/colecao", json={"id_dados_forma_atual": 1, "id_metodo_obtencao": 2},
        headers={"X-CSRF-Token": get_csrf(client)})
    assert response.status_code == 201
    assert response.get_json()["id_metodo_obtencao"] == 2


def test_fixture_loading_is_repeatable(app):
    with app.app_context():
        db = get_db()
        fixture = (Path(__file__).parent / "fixtures" / "catalog.sql").read_text()
        db.executescript(fixture)
        db.executescript(fixture)
        assert db.execute("SELECT count(*) FROM ESPECIE").fetchone()[0] == 1
        assert db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO").fetchone()[0] == 1


def test_profile_repository_enforces_private_reads_and_context(app):
    from pokeanalyzer.dao import PerfilDAO
    from pokeanalyzer.services import AuthService, PerfilService
    with app.app_context():
        first = AuthService().cadastrar("fixture_one", "one@example.invalid", "fixture_password")
        second = AuthService().cadastrar("fixture_two", "two@example.invalid", "fixture_password")
        profile = PerfilService().criar_personalizado(first.id_usuario, {
            "id_dados_forma": 1, "id_mecanica": 1, "nome_perfil": "FIXTURE private"})
        assert PerfilDAO().obter_visivel(profile.id_perfil, first.id_usuario) == profile
        assert PerfilDAO().obter_visivel(profile.id_perfil, second.id_usuario) is None
        assert PerfilDAO().obter_visivel(profile.id_perfil) is None
        with pytest.raises(ValueError, match="incompatível"):
            PerfilService().criar_personalizado(first.id_usuario, {
                "id_dados_forma": 1, "id_mecanica": 999, "nome_perfil": "FIXTURE invalid"})
