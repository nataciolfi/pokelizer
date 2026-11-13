"""DAOs: toda consulta SQL fica concentrada nesta camada."""

import sqlite3
from typing import Any

from .db import get_db, transaction
from .models import PokemonCatalogo, PokemonColecao, Usuario


class UsuarioDAO:
    def criar(self, nome_usuario: str, email: str, senha_hash: str) -> Usuario:
        connection = get_db()
        with transaction(connection):
            cursor = connection.execute(
                """INSERT INTO USUARIO (nome_usuario, email, senha_hash)
                   VALUES (?, ?, ?)""",
                (nome_usuario, email, senha_hash),
            )
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
               FROM ESPECIE e
               LEFT JOIN FORMA f ON f.id_especie = e.id_especie
               LEFT JOIN DADOS_FORMA_JOGO dfj ON dfj.id_forma = f.id_forma
               LEFT JOIN JOGO j ON j.id_jogo = dfj.id_jogo"""

    def listar(self, busca: str | None = None, *, tipo: int | None = None,
               geracao: int | None = None, jogo: int | None = None) -> list[PokemonCatalogo]:
        conditions, params = [], []
        if busca:
            term = busca.strip()
            conditions.append("(e.nome_pt LIKE ? OR e.nome_en LIKE ? OR f.nome_forma LIKE ? OR CAST(e.numero_nacional AS TEXT) = ?)")
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%", term])
        if tipo is not None:
            conditions.append("EXISTS (SELECT 1 FROM TIPO_FORMA_JOGO t WHERE t.id_dados_forma=dfj.id_dados_forma AND t.id_tipo=?)")
            params.append(tipo)
        if geracao is not None:
            conditions.append("e.geracao_origem = ?")
            params.append(geracao)
        if jogo is not None:
            conditions.append("dfj.id_jogo = ?")
            params.append(jogo)
        sql = self._SELECT + (" WHERE " + " AND ".join(conditions) if conditions else "")
        sql += " ORDER BY e.numero_nacional, f.nome_forma, j.nome"
        return [self._row_to_model(row) for row in get_db().execute(sql, params)]

    def obter(self, id_dados_forma: int) -> PokemonCatalogo | None:
        row = get_db().execute(self._SELECT + " WHERE dfj.id_dados_forma = ?", (id_dados_forma,)).fetchone()
        return self._row_to_model(row) if row else None

    @staticmethod
    def _row_to_model(row: sqlite3.Row) -> PokemonCatalogo:
        tipos_rows = get_db().execute(
            """SELECT t.nome_tipo FROM TIPO_FORMA_JOGO tfj
               JOIN TIPO t ON t.id_tipo = tfj.id_tipo
               WHERE tfj.id_dados_forma = ? ORDER BY tfj.posicao""",
            (row["id_dados_forma"],),
        ).fetchall()
        return PokemonCatalogo(**dict(row), tipos=tuple(item["nome_tipo"] for item in tipos_rows))


class ColecaoDAO:
    _SELECT = """SELECT pc.id_pokemon_colecao, pc.id_usuario, pc.id_dados_forma_atual,
                      pc.id_jogo_origem, pc.id_metodo_obtencao, pc.id_natureza,
                      pc.id_habilidade_forma, pc.apelido, pc.nivel, pc.data_registro,
                      pc.observacao, pc.id_mecanica, pc.id_dados_forma_origem, e.nome_pt, f.nome_forma, j_atual.nome AS nome_jogo_atual,
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
        with transaction(connection):
            cursor = connection.execute(
                """INSERT INTO POKEMON_COLECAO (
                       id_usuario, id_dados_forma_atual, id_jogo_origem,
                       id_metodo_obtencao, id_natureza, id_habilidade_forma,
                       apelido, nivel, observacao, id_mecanica, id_dados_forma_origem
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (dados["id_usuario"], dados["id_dados_forma_atual"],
                 dados.get("id_jogo_origem"), dados.get("id_metodo_obtencao"),
                 dados.get("id_natureza"), dados.get("id_habilidade_forma"),
                 dados.get("apelido"), dados.get("nivel"), dados.get("observacao"),
                 dados.get("id_mecanica"), dados.get("id_dados_forma_origem")),
            )
            pokemon = self.obter_do_usuario(cursor.lastrowid, dados["id_usuario"])
        return pokemon

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
        connection = get_db()
        with transaction(connection):
            cursor = connection.execute(
                "DELETE FROM POKEMON_COLECAO WHERE id_pokemon_colecao = ? AND id_usuario = ?",
                (id_pokemon, id_usuario),
            )
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


class PerfilDAO:
    """Visibility checks belong to every profile read, not only HTTP routes."""

    def obter_visivel(self, id_perfil: int, id_usuario: int | None = None):
        from .models import PerfilAnalise
        row = get_db().execute(
            """SELECT * FROM PERFIL_ANALISE WHERE id_perfil=? AND
               (tipo_perfil='referencia_competitiva' OR
                (tipo_perfil='personalizado' AND id_usuario=?))""",
            (id_perfil, id_usuario),
        ).fetchone()
        return PerfilAnalise(**dict(row)) if row else None

    def criar_personalizado(self, id_usuario: int, id_dados_forma: int,
                           id_mecanica: int, nome: str, id_regulamento: int | None = None):
        connection = get_db()
        with transaction(connection):
            cursor = connection.execute(
                """INSERT INTO PERFIL_ANALISE
                   (id_usuario,id_dados_forma,id_mecanica,nome_perfil,id_regulamento,tipo_perfil)
                   VALUES (?,?,?,?,?,'personalizado')""",
                (id_usuario, id_dados_forma, id_mecanica, nome, id_regulamento),
            )
            result = self.obter_visivel(cursor.lastrowid, id_usuario)
        return result
