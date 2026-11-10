"""Rotas REST da API. As rotas só fazem HTTP e delegam regras aos serviços."""

import secrets
import sqlite3
from functools import wraps
from typing import Callable

from flask import Blueprint, current_app, jsonify, request, session

from .dao import ColecaoDAO, PokemonDAO, UsuarioDAO
from .services import AuthService, ColecaoService

api = Blueprint("api", __name__)


def _json_data() -> dict:
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


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
        if not expected or not secrets.compare_digest(expected, supplied):
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
    busca = request.args.get("busca", "").strip() or None
    pokemon = PokemonDAO().listar(busca)
    return jsonify({"itens": [item.to_dict() for item in pokemon], "total": len(pokemon)})


@api.get("/pokemon/<int:id_dados_forma>")
def obter_pokemon(id_dados_forma: int):
    pokemon = PokemonDAO().obter(id_dados_forma)
    if not pokemon:
        return jsonify({"erro": "Registro de Pokémon não encontrado."}), 404
    return jsonify(pokemon.to_dict())


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
    excluido = ColecaoDAO().excluir_do_usuario(id_pokemon, session["id_usuario"])
    if not excluido:
        return jsonify({"erro": "Registro não encontrado."}), 404
    return jsonify({"mensagem": "Registro removido."})
