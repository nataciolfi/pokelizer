"""Testes de integração da API usando um banco SQLite temporário."""

import pytest

from pokeanalyzer import create_app
from pokeanalyzer.db import get_db


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.sqlite3"
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "DATABASE": str(database),
        "SESSION_COOKIE_SECURE": False,
    })
    with app.app_context():
        db = get_db()
        db.executescript(
            """
            INSERT INTO ESPECIE (numero_nacional, nome_pt, nome_en, geracao_origem)
            VALUES (25, 'Pikachu', 'Pikachu', 1);
            INSERT INTO FORMA (id_especie, codigo_forma, nome_forma, categoria, forma_padrao)
            VALUES (1, 'padrao', 'Padrão', 'padrao', 1);
            INSERT INTO JOGO (nome, categoria, geracao, plataforma)
            VALUES ('Jogo de teste', 'teste', 9, 'plataforma de teste');
            INSERT INTO DADOS_FORMA_JOGO (id_forma, id_jogo, status_presenca, pode_ser_registrada)
            VALUES (1, 1, 'nativa', 'sim');
            INSERT INTO TIPO (nome_tipo) VALUES ('Elétrico');
            INSERT INTO TIPO_FORMA_JOGO (id_dados_forma, id_tipo, posicao) VALUES (1, 1, 1);
            INSERT INTO METODO_OBTENCAO (nome) VALUES ('captura');
            INSERT INTO METODO_FORMA_JOGO (id_dados_forma, id_metodo) VALUES (1, 1);
            INSERT INTO HABILIDADE (nome) VALUES ('Estática');
            INSERT INTO HABILIDADE_FORMA_JOGO (id_dados_forma, id_habilidade, slot)
            VALUES (1, 1, 'normal');
            """
        )
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
    response = client.get("/api/pokemon?busca=Pika")
    assert response.status_code == 200
    assert response.get_json()["total"] == 1
    assert response.get_json()["itens"][0]["tipos"] == ["Elétrico"]


def test_register_and_private_collection_crud(client):
    create_user(client)
    token = get_csrf(client)

    added = client.post(
        "/api/colecao",
        json={
            "id_dados_forma_atual": 1,
            "id_metodo_obtencao": 1,
            "id_habilidade_forma": 1,
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
        db.execute("UPDATE DADOS_FORMA_JOGO SET status_presenca = 'ausente' WHERE id_dados_forma = 1")
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
