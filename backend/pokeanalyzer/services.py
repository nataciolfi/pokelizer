"""Regras de negócio: validação e autenticação ficam fora das rotas."""

import re
import sqlite3
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from .dao import ColecaoDAO, UsuarioDAO
from .models import PokemonColecao, Usuario


class AuthService:
    def __init__(self, usuario_dao: UsuarioDAO | None = None):
        self.usuario_dao = usuario_dao or UsuarioDAO()

    def cadastrar(self, nome_usuario: str, email: str, senha: str) -> Usuario:
        if not isinstance(nome_usuario, str) or not isinstance(email, str) or not isinstance(senha, str):
            raise ValueError("Nome de usuário, e-mail e senha devem ser textos.")
        nome_usuario = nome_usuario.strip()
        email = email.strip().lower()

        if len(nome_usuario) < 3:
            raise ValueError("O nome de usuário deve ter pelo menos 3 caracteres.")
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise ValueError("Informe um endereço de e-mail válido.")
        if len(senha) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")

        senha_hash = generate_password_hash(senha, method="scrypt")
        try:
            return self.usuario_dao.criar(nome_usuario, email, senha_hash)
        except sqlite3.IntegrityError as exc:
            raise ValueError("Este nome de usuário ou e-mail já está cadastrado.") from exc

    def autenticar(self, email: str, senha: str) -> Usuario | None:
        if not isinstance(email, str) or not isinstance(senha, str):
            return None
        usuario = self.usuario_dao.obter_por_email(email.strip())
        if not usuario or not usuario.senha_hash:
            return None
        if not check_password_hash(usuario.senha_hash, senha):
            return None
        return self.usuario_dao.obter_por_id(usuario.id_usuario)


class ColecaoService:
    def __init__(self, colecao_dao: ColecaoDAO | None = None):
        self.colecao_dao = colecao_dao or ColecaoDAO()

    def adicionar(self, id_usuario: int, dados: dict[str, Any]) -> PokemonColecao:
        try:
            id_dados_forma = int(dados["id_dados_forma_atual"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("id_dados_forma_atual é obrigatório e deve ser inteiro.") from exc

        nivel = dados.get("nivel")
        if nivel is not None:
            try:
                nivel = int(nivel)
            except (TypeError, ValueError) as exc:
                raise ValueError("O nível deve ser um número inteiro entre 1 e 100.") from exc
            if not 1 <= nivel <= 100:
                raise ValueError("O nível deve estar entre 1 e 100.")

        apelido = self._texto_opcional(dados.get("apelido"), "apelido", 40)
        observacao = self._texto_opcional(dados.get("observacao"), "observacao", 500)

        contexto = self.colecao_dao.obter_contexto_registro(id_dados_forma)
        if not contexto:
            raise ValueError("A ficha de forma/jogo informada não existe.")
        if contexto["status_presenca"] == "ausente" or contexto["pode_ser_registrada"] == "nao":
            raise ValueError("Esta forma não pode ser registrada neste contexto de jogo.")

        if dados.get("id_metodo_obtencao") is not None:
            try:
                metodo = int(dados["id_metodo_obtencao"])
            except (TypeError, ValueError) as exc:
                raise ValueError("id_metodo_obtencao deve ser inteiro.") from exc
            if not self.colecao_dao.metodo_disponivel(id_dados_forma, metodo):
                raise ValueError("O método de obtenção não está cadastrado para esta forma/jogo.")
        else:
            metodo = None

        if dados.get("id_habilidade_forma") is not None:
            try:
                habilidade = int(dados["id_habilidade_forma"])
            except (TypeError, ValueError) as exc:
                raise ValueError("id_habilidade_forma deve ser inteiro.") from exc
            if not self.colecao_dao.habilidade_compativel(id_dados_forma, habilidade):
                raise ValueError("A habilidade não está disponível para esta forma/jogo.")
        else:
            habilidade = None

        valores = {
            "id_usuario": id_usuario,
            "id_dados_forma_atual": id_dados_forma,
            "id_jogo_origem": self._id_opcional(dados.get("id_jogo_origem"), "id_jogo_origem"),
            "id_metodo_obtencao": metodo,
            "id_natureza": self._id_opcional(dados.get("id_natureza"), "id_natureza"),
            "id_habilidade_forma": habilidade,
            "apelido": apelido,
            "nivel": nivel,
            "observacao": observacao,
        }
        try:
            return self.colecao_dao.adicionar(valores)
        except sqlite3.IntegrityError as exc:
            raise ValueError("Não foi possível cadastrar: confira se todos os IDs relacionados existem.") from exc

    @staticmethod
    def _id_opcional(valor: Any, campo: str) -> int | None:
        if valor is None:
            return None
        try:
            return int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{campo} deve ser inteiro.") from exc

    @staticmethod
    def _texto_opcional(valor: Any, campo: str, limite: int) -> str | None:
        if valor is None or valor == "":
            return None
        if not isinstance(valor, str):
            raise ValueError(f"{campo} deve ser texto.")
        valor = valor.strip()
        if len(valor) > limite:
            raise ValueError(f"{campo} deve ter no máximo {limite} caracteres.")
        return valor or None
