"""Modelos de domínio usados pela camada de serviços e pelos DAOs."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Usuario:
    id_usuario: int
    nome_usuario: str
    email: str
    data_cadastro: str
    senha_hash: str | None = None

    def to_public_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("senha_hash", None)
        return data


@dataclass(frozen=True)
class PokemonCatalogo:
    id_dados_forma: int | None
    id_especie: int
    id_forma: int | None
    id_jogo: int | None
    numero_nacional: int
    nome_pt: str
    nome_forma: str | None
    nome_jogo: str | None
    status_presenca: str | None
    pode_ser_registrada: str | None
    tipos: tuple[str, ...] = ()
    codigo_forma: str | None = None
    nome_en: str | None = None
    fonte_url: str | None = None
    data_verificacao: str | None = None
    fichas: tuple[dict[str, Any], ...] = ()
    fonte_forma_url: str | None = None
    data_verificacao_forma: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tipos"] = list(self.tipos)
        return data


@dataclass(frozen=True)
class PokemonColecao:
    id_pokemon_colecao: int
    id_usuario: int
    id_dados_forma_atual: int
    id_jogo_origem: int | None
    id_metodo_obtencao: int | None
    id_natureza: int | None
    id_habilidade_forma: int | None
    apelido: str | None
    nivel: int | None
    data_registro: str
    observacao: str | None
    nome_pt: str
    nome_forma: str | None
    nome_jogo_atual: str
    nome_jogo_origem: str | None
    nome_metodo: str | None
    nome_natureza: str | None
    nome_habilidade: str | None
    id_mecanica: int | None = None
    id_dados_forma_origem: int | None = None
    valores: tuple[dict[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PerfilAnalise:
    """Profile identity/context; target values and options stay in related tables."""
    id_perfil: int
    id_dados_forma: int
    id_mecanica: int
    id_usuario: int | None
    id_regulamento: int | None
    nome_perfil: str
    descricao: str | None
    tipo_perfil: str
    fonte_url: str | None
    data_verificacao: str | None
    versao_fonte: str | None
    valores: tuple[dict[str, Any], ...] = ()
    naturezas: tuple[int, ...] = ()
    habilidades: tuple[int, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
