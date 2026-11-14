"""Rotas REST da API. As rotas só fazem HTTP e delegam regras aos serviços."""

import secrets
import sqlite3
from functools import wraps
from typing import Callable

from flask import Blueprint, current_app, jsonify, request, session

from .dao import ColecaoDAO, PokemonDAO, UsuarioDAO, PerfilDAO, ContextoDAO, RegulamentoDAO
from .services import AuthService, ColecaoService, PerfilService, ComparacaoService, validar_campos

api = Blueprint("api", __name__)


def _json_data() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("O corpo deve ser um objeto JSON válido.")
    return data


def csrf_token() -> str:
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def csrf_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        expected = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token", "")
        if not expected or not secrets.compare_digest(expected.encode("utf-8"), supplied.encode("utf-8")):
            return jsonify({"erro": "Token CSRF ausente ou inválido."}), 403
        return view(*args, **kwargs)
    return wrapped


def login_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("id_usuario"):
            return jsonify({"erro": "Autenticação necessária."}), 401
        return view(*args, **kwargs)
    return wrapped


@api.get("/status")
def status():
    return jsonify({"status": "ok", "servico": "PokéAnalyzer API"})


@api.get("/csrf")
def get_csrf():
    return jsonify({"csrf_token": csrf_token()})


@api.post("/auth/cadastro")
@csrf_required
def cadastro():
    data = _json_data()
    validar_campos(data, {"nome_usuario", "email", "senha"})
    try:
        usuario = AuthService().cadastrar(
            data.get("nome_usuario", ""), data.get("email", ""), data.get("senha", "")
        )
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400

    session.clear()
    session["id_usuario"] = usuario.id_usuario
    token = csrf_token()
    return jsonify({"usuario": usuario.to_public_dict(), "csrf_token": token}), 201


@api.post("/auth/login")
@csrf_required
def login():
    data = _json_data()
    validar_campos(data, {"email", "senha"})
    usuario = AuthService().autenticar(data.get("email", ""), data.get("senha", ""))
    if not usuario:
        return jsonify({"erro": "E-mail ou senha inválidos."}), 401

    session.clear()
    session["id_usuario"] = usuario.id_usuario
    token = csrf_token()
    return jsonify({"usuario": usuario.to_public_dict(), "csrf_token": token}), 200


@api.post("/auth/logout")
@csrf_required
@login_required
def logout():
    if request.data:
        validar_campos(_json_data(), set())
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada."})


@api.get("/auth/me")
@login_required
def me():
    usuario = UsuarioDAO().obter_por_id(session["id_usuario"])
    if not usuario:
        session.clear()
        return jsonify({"erro": "Usuário não encontrado."}), 401
    return jsonify({"usuario": usuario.to_public_dict()})


@api.get("/pokemon")
def listar_pokemon():
    validar_campos(request.args, {"busca", "tipo", "geracao", "jogo"})
    if any(len(request.args.getlist(k)) != 1 for k in request.args):
        raise ValueError("Filtros repetidos não são suportados.")
    busca = request.args.get("busca", "").strip() or None
    try:
        filters = {key: ColecaoService._id_opcional(request.args.get(key), key)
                   for key in ("tipo", "geracao", "jogo")}
        pokemon = PokemonDAO().listar_global(busca, **filters)
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400
    return jsonify({"itens": [item.to_dict() for item in pokemon], "total": len(pokemon)})


@api.get("/pokemon/<int:id_dados_forma>")
def obter_pokemon(id_dados_forma: int):
    pokemon = ContextoDAO().ficha(id_dados_forma)
    if not pokemon:
        return jsonify({"erro": "Registro de Pokémon não encontrado."}), 404
    return jsonify(pokemon)


@api.get("/colecao")
@login_required
def listar_colecao():
    itens = ColecaoDAO().listar_do_usuario(session["id_usuario"])
    return jsonify({"itens": [item.to_dict() for item in itens], "total": len(itens)})


@api.post("/colecao")
@login_required
@csrf_required
def adicionar_colecao():
    try:
        pokemon = ColecaoService().adicionar(session["id_usuario"], _json_data())
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400
    except sqlite3.IntegrityError:
        current_app.logger.exception("Falha de integridade ao inserir na coleção")
        return jsonify({"erro": "Falha de integridade ao inserir na coleção."}), 400
    return jsonify(pokemon.to_dict()), 201


@api.get("/colecao/<int:id_pokemon>")
@login_required
def obter_colecao(id_pokemon: int):
    pokemon = ColecaoDAO().obter_do_usuario(id_pokemon, session["id_usuario"])
    if not pokemon:
        return jsonify({"erro": "Registro não encontrado."}), 404
    return jsonify(pokemon.to_dict())


@api.delete("/colecao/<int:id_pokemon>")
@login_required
@csrf_required
def excluir_colecao(id_pokemon: int):
    if request.data:
        validar_campos(_json_data(), set())
    excluido = ColecaoDAO().excluir_do_usuario(id_pokemon, session["id_usuario"])
    if not excluido:
        return jsonify({"erro": "Registro não encontrado."}), 404
    return jsonify({"mensagem": "Registro removido."})


@api.before_request
def validar_consulta():
    if request.endpoint != "api.listar_pokemon" and request.args:
        raise ValueError("Esta rota não aceita parâmetros de consulta.")


@api.errorhandler(ValueError)
def validation_error(exc):
    return jsonify({"erro": str(exc)}), 400


@api.errorhandler(LookupError)
def not_found(exc):
    return jsonify({"erro": str(exc)}), 404


@api.patch("/colecao/<int:id_pokemon>")
@login_required
@csrf_required
def editar_colecao(id_pokemon):
    return jsonify(ColecaoService().editar(session["id_usuario"], id_pokemon, _json_data()).to_dict())


@api.get("/perfis")
@login_required
def listar_perfis():
    items = PerfilDAO().listar_visiveis(session["id_usuario"])
    return jsonify({"itens": [p.to_dict() for p in items], "total": len(items)})


@api.post("/perfis")
@login_required
@csrf_required
def criar_perfil():
    return jsonify(PerfilService().criar_personalizado(session["id_usuario"], _json_data()).to_dict()), 201


@api.get("/perfis/<int:id_perfil>")
@login_required
def obter_perfil(id_perfil):
    item = PerfilDAO().obter_visivel(id_perfil, session["id_usuario"])
    if not item:
        raise LookupError("Perfil não encontrado.")
    return jsonify(item.to_dict())


@api.patch("/perfis/<int:id_perfil>")
@login_required
@csrf_required
def editar_perfil(id_perfil):
    return jsonify(PerfilService().editar(session["id_usuario"], id_perfil, _json_data()).to_dict())


@api.delete("/perfis/<int:id_perfil>")
@login_required
@csrf_required
def excluir_perfil(id_perfil):
    if request.data:
        validar_campos(_json_data(), set())
    if not PerfilDAO().excluir_personalizado(id_perfil, session["id_usuario"]):
        raise LookupError("Perfil não encontrado.")
    return jsonify({"mensagem": "Perfil removido."})


@api.post("/analises")
@login_required
@csrf_required
def analisar():
    data = _json_data()
    validar_campos(data, {"id_pokemon_colecao", "id_perfil"})
    ids = [ColecaoService._id_opcional(data.get(k), k) for k in ("id_pokemon_colecao", "id_perfil")]
    if None in ids:
        raise ValueError("Exemplar e perfil são obrigatórios.")
    return jsonify(ComparacaoService().comparar(session["id_usuario"], *ids))


@api.get("/formas/<int:id_forma>")
def obter_forma(id_forma):
    item = PokemonDAO().obter_forma(id_forma)
    if not item:
        raise LookupError("Forma não encontrada.")
    return jsonify(item)


@api.get("/opcoes")
def opcoes():
    return jsonify(ContextoDAO().opcoes())


@api.get("/mecanicas/<int:id_mecanica>")
def obter_mecanica(id_mecanica):
    item = ContextoDAO().mecanica(id_mecanica)
    if not item:
        raise LookupError("Mecânica não encontrada.")
    return jsonify(item)


@api.get("/regulamentos")
def listar_regulamentos():
    items = RegulamentoDAO().listar()
    return jsonify({"itens": items, "total": len(items)})


@api.get("/regulamentos/<int:id_regulamento>/formas/<int:id_dados_forma>")
def elegibilidade(id_regulamento, id_dados_forma):
    return jsonify(RegulamentoDAO().elegibilidade(id_regulamento, id_dados_forma))


@api.get("/catalogo/cobertura")
def cobertura_catalogo():
    from .catalog_data import cobertura
    return jsonify(cobertura())
