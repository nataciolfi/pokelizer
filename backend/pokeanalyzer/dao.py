"""DAOs: toda consulta SQL fica concentrada nesta camada."""

import sqlite3
from typing import Any

from .db import get_db
from .models import PokemonCatalogo, PokemonColecao, Usuario


class UsuarioDAO:
    def criar(self, nome_usuario: str, email: str, senha_hash: str) -> Usuario:
        connection = get_db()
        cursor = connection.execute(
            """INSERT INTO USUARIO (nome_usuario, email, senha_hash)
               VALUES (?, ?, ?)""",
            (nome_usuario, email, senha_hash),
        )
        connection.commit()
        return self.obter_por_id(cursor.lastrowid)  # type: ignore[return-value]

    def obter_por_email(self, email: str) -> Usuario | None:
        row = get_db().execute(
            """SELECT id_usuario, nome_usuario, email, senha_hash, data_cadastro
               FROM USUARIO WHERE email = ? COLLATE NOCASE""",
            (email,),
        ).fetchone()
        return Usuario(**dict(row)) if row else None

    def obter_por_id(self, id_usuario: int) -> Usuario | None:
        row = get_db().execute(
            """SELECT id_usuario, nome_usuario, email, data_cadastro
               FROM USUARIO WHERE id_usuario = ?""",
            (id_usuario,),
        ).fetchone()
        return Usuario(**dict(row)) if row else None


class PokemonDAO:
    _SELECT = """SELECT dfj.id_dados_forma, e.id_especie, f.id_forma, j.id_jogo,
                      e.numero_nacional, e.nome_pt, f.nome_forma, j.nome AS nome_jogo,
                      dfj.status_presenca, dfj.pode_ser_registrada
               FROM DADOS_FORMA_JOGO dfj
               JOIN FORMA f ON f.id_forma = dfj.id_forma
               JOIN ESPECIE e ON e.id_especie = f.id_especie
               JOIN JOGO j ON j.id_jogo = dfj.id_jogo"""

    def listar(self, busca: str | None = None) -> list[PokemonCatalogo]:
        sql = self._SELECT
        params: tuple[Any, ...] = ()
        if busca:
            sql += " WHERE e.nome_pt LIKE ? OR f.nome_forma LIKE ?"
            termo = f"%{busca.strip()}%"
            params = (termo, termo)
        sql += " ORDER BY e.numero_nacional, f.nome_forma, j.nome"
        rows = get_db().execute(sql, params).fetchall()
        return [self._row_to_model(row) for row in rows]

    def obter(self, id_dados_forma: int) -> PokemonCatalogo | None:
        row = get_db().execute(
            self._SELECT + " WHERE dfj.id_dados_forma = ?",
            (id_dados_forma,),
        ).fetchone()
        return self._row_to_model(row) if row else None

    @staticmethod
    def _row_to_model(row: sqlite3.Row) -> PokemonCatalogo:
        tipos_rows = get_db().execute(
            """SELECT t.nome_tipo FROM TIPO_FORMA_JOGO tfj
               JOIN TIPO t ON t.id_tipo = tfj.id_tipo
               WHERE tfj.id_dados_forma = ? ORDER BY tfj.posicao""",
            (row["id_dados_forma"],),
        ).fetchall()
        data = dict(row)
        return PokemonCatalogo(**data, tipos=tuple(item["nome_tipo"] for item in tipos_rows))


class ColecaoDAO:
    _SELECT = """SELECT pc.id_pokemon_colecao, pc.id_usuario, pc.id_dados_forma_atual,
                      pc.id_jogo_origem, pc.id_metodo_obtencao, pc.id_natureza,
                      pc.id_habilidade_forma, pc.apelido, pc.nivel, pc.data_registro,
                      pc.observacao, e.nome_pt, f.nome_forma, j_atual.nome AS nome_jogo_atual,
                      j_origem.nome AS nome_jogo_origem, mo.nome AS nome_metodo,
                      n.nome AS nome_natureza, h.nome AS nome_habilidade
               FROM POKEMON_COLECAO pc
               JOIN DADOS_FORMA_JOGO dfj ON dfj.id_dados_forma = pc.id_dados_forma_atual
               JOIN FORMA f ON f.id_forma = dfj.id_forma
               JOIN ESPECIE e ON e.id_especie = f.id_especie
               JOIN JOGO j_atual ON j_atual.id_jogo = dfj.id_jogo
               LEFT JOIN JOGO j_origem ON j_origem.id_jogo = pc.id_jogo_origem
               LEFT JOIN METODO_OBTENCAO mo ON mo.id_metodo = pc.id_metodo_obtencao
               LEFT JOIN NATUREZA n ON n.id_natureza = pc.id_natureza
               LEFT JOIN HABILIDADE_FORMA_JOGO hf ON hf.id_habilidade_forma = pc.id_habilidade_forma
               LEFT JOIN HABILIDADE h ON h.id_habilidade = hf.id_habilidade"""

    def adicionar(self, dados: dict[str, Any]) -> PokemonColecao:
        connection = get_db()
        cursor = connection.execute(
            """INSERT INTO POKEMON_COLECAO (
                   id_usuario, id_dados_forma_atual, id_jogo_origem,
                   id_metodo_obtencao, id_natureza, id_habilidade_forma,
                   apelido, nivel, observacao
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                dados["id_usuario"], dados["id_dados_forma_atual"],
                dados.get("id_jogo_origem"), dados.get("id_metodo_obtencao"),
                dados.get("id_natureza"), dados.get("id_habilidade_forma"),
                dados.get("apelido"), dados.get("nivel"), dados.get("observacao"),
            ),
        )
        connection.commit()
        return self.obter_do_usuario(cursor.lastrowid, dados["id_usuario"])  # type: ignore[return-value]

    def listar_do_usuario(self, id_usuario: int) -> list[PokemonColecao]:
        rows = get_db().execute(
            self._SELECT + " WHERE pc.id_usuario = ? ORDER BY pc.id_pokemon_colecao DESC",
            (id_usuario,),
        ).fetchall()
        return [PokemonColecao(**dict(row)) for row in rows]

    def obter_do_usuario(self, id_pokemon: int, id_usuario: int) -> PokemonColecao | None:
        row = get_db().execute(
            self._SELECT + " WHERE pc.id_pokemon_colecao = ? AND pc.id_usuario = ?",
            (id_pokemon, id_usuario),
        ).fetchone()
        return PokemonColecao(**dict(row)) if row else None

    def excluir_do_usuario(self, id_pokemon: int, id_usuario: int) -> bool:
        cursor = get_db().execute(
            "DELETE FROM POKEMON_COLECAO WHERE id_pokemon_colecao = ? AND id_usuario = ?",
            (id_pokemon, id_usuario),
        )
        get_db().commit()
        return cursor.rowcount > 0

    def obter_contexto_registro(self, id_dados_forma: int) -> dict[str, Any] | None:
        row = get_db().execute(
            """SELECT status_presenca, pode_ser_registrada
               FROM DADOS_FORMA_JOGO WHERE id_dados_forma = ?""",
            (id_dados_forma,),
        ).fetchone()
        return dict(row) if row else None

    def metodo_disponivel(self, id_dados_forma: int, id_metodo: int) -> bool:
        row = get_db().execute(
            """SELECT 1 FROM METODO_FORMA_JOGO
               WHERE id_dados_forma = ? AND id_metodo = ?""",
            (id_dados_forma, id_metodo),
        ).fetchone()
        return row is not None

    def habilidade_compativel(self, id_dados_forma: int, id_habilidade_forma: int) -> bool:
        row = get_db().execute(
            """SELECT 1 FROM HABILIDADE_FORMA_JOGO
               WHERE id_dados_forma = ? AND id_habilidade_forma = ?""",
            (id_dados_forma, id_habilidade_forma),
        ).fetchone()
        return row is not None
