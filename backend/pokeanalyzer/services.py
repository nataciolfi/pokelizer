"""Regras de negócio: validação e autenticação ficam fora das rotas."""

import re
import sqlite3
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from .dao import ColecaoDAO, UsuarioDAO, PerfilDAO, ValorDAO, ContextoDAO, RegulamentoDAO
from .db import get_db, transaction
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

    CAMPOS = {"id_dados_forma_atual", "id_mecanica", "id_dados_forma_origem", "id_jogo_origem",
              "id_metodo_obtencao", "id_natureza", "id_habilidade_forma", "apelido", "nivel", "observacao", "valores"}

    def adicionar(self, id_usuario: int, dados: dict[str, Any]) -> PokemonColecao:
        validar_campos(dados, self.CAMPOS)
        values = validar_valores(dados.get("valores", []), "valor")
        try:
            with transaction(get_db()):
                pokemon = self.colecao_dao.adicionar(self._preparar(id_usuario, dados))
                ValorDAO().substituir("pokemon", pokemon.id_pokemon_colecao, values)
                return self.colecao_dao.obter_do_usuario(pokemon.id_pokemon_colecao, id_usuario)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Cadastro incompatível com as regras do banco: {exc}") from exc

    def editar(self, id_usuario, id_pokemon, dados):
        validar_campos(dados, self.CAMPOS)
        if not dados:
            raise ValueError("Informe ao menos um campo para editar.")
        try:
            with transaction(get_db()):
                current = self.colecao_dao.obter_do_usuario(id_pokemon, id_usuario)
                if not current:
                    raise LookupError("Registro não encontrado.")
                merged = {k: current.to_dict().get(k) for k in self.CAMPOS - {"valores"}}
                merged.update(dados)
                changed = any(merged[k] != getattr(current, k) for k in ("id_mecanica", "id_dados_forma_atual"))
                if changed and current.valores and "valores" not in dados:
                    raise ValueError("Mudança de contexto exige valores explícitos, inclusive [] para removê-los.")
                # Remove children before changing a context; transaction restores all on failure.
                if "valores" in dados:
                    values = validar_valores(dados["valores"], "valor")
                    ValorDAO().substituir("pokemon", id_pokemon, [])
                self.colecao_dao.atualizar_do_usuario(id_pokemon, id_usuario, self._preparar(id_usuario, merged))
                if "valores" in dados:
                    ValorDAO().substituir("pokemon", id_pokemon, values)
                return self.colecao_dao.obter_do_usuario(id_pokemon, id_usuario)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Edição incompatível com as regras do banco: {exc}") from exc

    def _preparar(self, id_usuario: int, dados: dict[str, Any]):
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
        return valores

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


def validar_campos(dados, permitidos):
    if not isinstance(dados, dict):
        raise ValueError("O corpo deve ser um objeto JSON.")
    extra = set(dados) - permitidos
    if extra:
        raise ValueError("Campos não reconhecidos ou não suportados: " + ", ".join(sorted(extra)))


def validar_valores(valores, campo):
    if not isinstance(valores, list):
        raise ValueError("valores deve ser uma lista; [] remove todos os valores.")
    result, keys = [], set()
    for value in valores:
        validar_campos(value, {"id_mecanica_sistema_atributo", "id_atributo", "estado", campo, "motivo"})
        ids = {k: ColecaoService._id_opcional(value.get(k), k) for k in ("id_mecanica_sistema_atributo", "id_atributo")}
        if None in ids.values():
            raise ValueError("Cada valor exige sistema da mecânica e atributo.")
        key = tuple(ids.values())
        if key in keys:
            raise ValueError("Atributo duplicado no mesmo sistema.")
        keys.add(key)
        estado = value.get("estado", "conhecido")
        if estado not in ("conhecido", "desconhecido", "nao_aplicavel"):
            raise ValueError("Estado de atributo inválido.")
        number = ColecaoService._inteiro_opcional(value.get(campo), campo, minimo=0)
        if (estado == "conhecido") != (number is not None):
            raise ValueError("Conhecido exige número; desconhecido/não aplicável exige valor nulo.")
        result.append(ids | {"estado": estado, campo: number,
            "motivo": ColecaoService._texto_opcional(value.get("motivo"), "motivo", 500)})
    return result


class PerfilService:
    CAMPOS = {"id_dados_forma", "id_mecanica", "id_regulamento", "nome_perfil", "descricao", "valores", "naturezas", "habilidades"}

    def __init__(self, perfil_dao=None):
        self.perfil_dao = perfil_dao or PerfilDAO()

    def _preparar(self, dados):
        fields = {f: ColecaoService._id_opcional(dados.get(f), f) for f in ("id_dados_forma", "id_mecanica", "id_regulamento")}
        if fields["id_dados_forma"] is None or fields["id_mecanica"] is None:
            raise ValueError("Perfil exige forma/jogo e versão da mecânica.")
        name = ColecaoService._texto_opcional(dados.get("nome_perfil"), "nome_perfil", 120)
        if not name:
            raise ValueError("nome_perfil é obrigatório.")
        fields.update(nome_perfil=name, descricao=ColecaoService._texto_opcional(dados.get("descricao"), "descricao", 2000))
        return fields

    @staticmethod
    def _opcoes(dados, key):
        options = dados.get(key, [])
        if not isinstance(options, list):
            raise ValueError(f"{key} deve ser uma lista de IDs.")
        ids = [ColecaoService._id_opcional(v, key) for v in options]
        if None in ids or len(set(ids)) != len(ids):
            raise ValueError(f"{key} exige IDs únicos e não nulos.")
        return ids

    def criar_personalizado(self, id_usuario, dados):
        validar_campos(dados, self.CAMPOS)
        fields = self._preparar(dados)
        values = validar_valores(dados.get("valores", []), "valor_alvo")
        natures, abilities = self._opcoes(dados, "naturezas"), self._opcoes(dados, "habilidades")
        try:
            with transaction(get_db()):
                profile = self.perfil_dao.criar_personalizado(id_usuario, fields["id_dados_forma"], fields["id_mecanica"], fields["nome_perfil"], fields["id_regulamento"])
                self.perfil_dao.atualizar_personalizado(profile.id_perfil, id_usuario, fields)
                ValorDAO().substituir("perfil", profile.id_perfil, values)
                self.perfil_dao.substituir_opcoes(profile.id_perfil, natures, abilities)
                return self.perfil_dao.obter_visivel(profile.id_perfil, id_usuario)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Perfil incompatível com as regras do banco: {exc}") from exc

    def editar(self, id_usuario, id_perfil, dados):
        validar_campos(dados, self.CAMPOS)
        if not dados:
            raise ValueError("Informe ao menos um campo para editar.")
        try:
            with transaction(get_db()):
                current = self.perfil_dao.obter_visivel(id_perfil, id_usuario)
                if not current or current.tipo_perfil != "personalizado" or current.id_usuario != id_usuario:
                    raise LookupError("Perfil não encontrado.")
                merged = current.to_dict() | dados
                changed = any(merged[k] != getattr(current, k) for k in ("id_dados_forma", "id_mecanica"))
                if changed and not {"valores", "naturezas", "habilidades"} <= dados.keys():
                    raise ValueError("Mudança de contexto exige valores, naturezas e habilidades explícitos.")
                values = validar_valores(dados["valores"] if "valores" in dados else list(current.valores), "valor_alvo")
                options = {k: self._opcoes({k: dados[k] if k in dados else list(getattr(current, k))}, k) for k in ("naturezas", "habilidades")}
                ValorDAO().substituir("perfil", id_perfil, [])
                self.perfil_dao.substituir_opcoes(id_perfil, [], [])
                self.perfil_dao.atualizar_personalizado(id_perfil, id_usuario, self._preparar(merged))
                ValorDAO().substituir("perfil", id_perfil, values)
                self.perfil_dao.substituir_opcoes(id_perfil, options["naturezas"], options["habilidades"])
                return self.perfil_dao.obter_visivel(id_perfil, id_usuario)
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"Perfil incompatível com as regras do banco: {exc}") from exc


class ComparacaoService:
    def comparar(self, id_usuario, id_pokemon, id_perfil):
        with transaction(get_db()):
            specimen = ColecaoDAO().obter_do_usuario(id_pokemon, id_usuario)
            profile = PerfilDAO().obter_visivel(id_perfil, id_usuario)
            if not specimen or not profile:
                raise LookupError("Exemplar ou perfil não encontrado.")
            if (specimen.id_dados_forma_atual, specimen.id_mecanica) != (profile.id_dados_forma, profile.id_mecanica):
                raise ValueError("Exemplar e perfil exigem a mesma forma/jogo e versão exata de mecânica.")
            mechanic = ContextoDAO().mecanica(profile.id_mecanica)
            actual = {(v["id_mecanica_sistema_atributo"], v["id_atributo"]): v for v in specimen.valores}
            targets = {(v["id_mecanica_sistema_atributo"], v["id_atributo"]): v for v in profile.valores}
            rows = []
            for system in mechanic["sistemas"]:
                for attr in system["atributos"]:
                    key = (system["id_mecanica_sistema_atributo"], attr["id_atributo"])
                    a, t = actual.get(key), targets.get(key)
                    real, target = a.get("valor") if a else None, t.get("valor_alvo") if t else None
                    difference = None
                    statuses = (system["aplicabilidade"], attr["aplicabilidade"])
                    if "nao_aplicavel" in statuses:
                        state = "nao_aplicavel"
                    elif "nao_verificado" in statuses:
                        state = "nao_verificado"
                    elif not t:
                        state = "nao_comparado"
                    elif target is None or real is None:
                        state = "sem_dado"
                    else:
                        difference = real - target
                        state = "igual" if difference == 0 else "abaixo" if difference < 0 else "acima"
                    rows.append({"id_mecanica_sistema_atributo": key[0], "sistema": system["codigo"],
                        "id_atributo": key[1], "atributo": attr["codigo"], "real": real, "alvo": target,
                        "estado_real": a["estado"] if a else "ausente", "estado_alvo": t["estado"] if t else "ausente",
                        "diferenca": difference, "estado": state})
            categorical = []
            for field, options, flag in (("id_natureza", profile.naturezas, "usa_natureza"),
                                          ("id_habilidade_forma", profile.habilidades, "usa_habilidade")):
                real = getattr(specimen, field)
                state = "nao_aplicavel" if mechanic[flag] == "nao" else "nao_verificado" if mechanic[flag] == "nao_verificado" else "nao_comparado" if not options else "sem_dado" if real is None else "preferida" if real in options else "nao_preferida"
                categorical.append({"campo": field, "real": real, "opcoes": list(options), "estado": state})
            eligibility = RegulamentoDAO().elegibilidade(profile.id_regulamento, profile.id_dados_forma) if profile.id_regulamento else None
            return {"id_pokemon_colecao": id_pokemon, "perfil": profile.to_dict(), "mecanica": mechanic,
                "campos": rows, "preferencias": categorical, "elegibilidade": eligibility,
                "interpretacao": "Diferença em relação ao alvo explícito. Acima ou abaixo não significa melhor ou pior.",
                "legalidade_completa_verificada": False}
