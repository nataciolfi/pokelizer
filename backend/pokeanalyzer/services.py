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
        if not isinstance(dados, dict):
            raise ValueError("Dados devem ser um objeto JSON.")
        id_dados_forma = self._id_opcional(dados.get("id_dados_forma_atual"), "id_dados_forma_atual")
        if id_dados_forma is None:
            raise ValueError("id_dados_forma_atual é obrigatório.")
        nivel = self._inteiro_opcional(dados.get("nivel"), "nivel", minimo=0)

        apelido = self._texto_opcional(dados.get("apelido"), "apelido", 40)
        observacao = self._texto_opcional(dados.get("observacao"), "observacao", 500)

        contexto = self.colecao_dao.obter_contexto_registro(id_dados_forma)
        if not contexto:
            raise ValueError("A ficha de forma/jogo informada não existe.")
        if contexto["status_presenca"] == "ausente" or contexto["pode_ser_registrada"] == "nao":
            raise ValueError("Esta forma não pode ser registrada neste contexto de jogo.")

        # The specimen's actual acquisition history is independent of availability
        # in its CURRENT game, which may have changed after a transfer.
        metodo = self._id_opcional(dados.get("id_metodo_obtencao"), "id_metodo_obtencao")

        if dados.get("id_habilidade_forma") is not None:
            habilidade = self._id_opcional(dados["id_habilidade_forma"], "id_habilidade_forma")
            if not self.colecao_dao.habilidade_compativel(id_dados_forma, habilidade):
                raise ValueError("A habilidade não está disponível para esta forma/jogo.")
        else:
            habilidade = None

        valores = {
            "id_usuario": id_usuario,
            "id_mecanica": self._id_opcional(dados.get("id_mecanica"), "id_mecanica"),
            "id_dados_forma_origem": self._id_opcional(dados.get("id_dados_forma_origem"), "id_dados_forma_origem"),
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
        return ColecaoService._inteiro_opcional(valor, campo, minimo=1)

    @staticmethod
    def _inteiro_opcional(valor: Any, campo: str, *, minimo: int) -> int | None:
        if valor is None:
            return None
        if isinstance(valor, bool) or not isinstance(valor, (int, str)):
            raise ValueError(f"{campo} deve ser inteiro >= {minimo}.")
        if isinstance(valor, str) and not re.fullmatch(r"[0-9]+", valor):
            raise ValueError(f"{campo} deve ser inteiro >= {minimo}.")
        number = int(valor)
        if not minimo <= number <= 2**63 - 1:
            raise ValueError(f"{campo} deve ser inteiro entre {minimo} e {2**63 - 1}.")
        return number

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


class PerfilService:
    """Initial profile persistence; comparison/calculation is planned for later stages."""

    def __init__(self, perfil_dao=None):
        from .dao import PerfilDAO
        self.perfil_dao = perfil_dao or PerfilDAO()

    def criar_personalizado(self, id_usuario: int, dados: dict[str, Any]):
        if not isinstance(dados, dict):
            raise ValueError("Dados devem ser um objeto.")
        fields = {field: ColecaoService._id_opcional(dados.get(field), field)
                  for field in ("id_dados_forma", "id_mecanica", "id_regulamento")}
        if fields["id_dados_forma"] is None or fields["id_mecanica"] is None:
            raise ValueError("Perfil exige forma/jogo e versão da mecânica.")
        nome = ColecaoService._texto_opcional(dados.get("nome_perfil"), "nome_perfil", 120)
        if not nome:
            raise ValueError("nome_perfil é obrigatório.")
        try:
            return self.perfil_dao.criar_personalizado(id_usuario, fields["id_dados_forma"],
                fields["id_mecanica"], nome, fields["id_regulamento"])
        except sqlite3.IntegrityError as exc:
            raise ValueError("Perfil incompatível: confira proprietário e contexto de jogo/mecânica/regulamento.") from exc
