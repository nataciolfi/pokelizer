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
    id_dados_forma: int
    id_especie: int
    id_forma: int
    id_jogo: int
    numero_nacional: int
    nome_pt: str
    nome_forma: str
    nome_jogo: str
    status_presenca: str
    pode_ser_registrada: str | None
    tipos: tuple[str, ...] = ()

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
    nome_forma: str
    nome_jogo_atual: str
    nome_jogo_origem: str | None
    nome_metodo: str | None
    nome_natureza: str | None
    nome_habilidade: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
