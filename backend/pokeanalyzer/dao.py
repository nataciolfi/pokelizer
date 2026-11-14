"""DAOs: toda consulta SQL fica concentrada nesta camada."""

import sqlite3
import csv
from functools import lru_cache
from pathlib import Path
from typing import Any

from .db import get_db, transaction
from .models import PokemonCatalogo, PokemonColecao, Usuario


@lru_cache(maxsize=1)
def _imagens_formas():
    """PokéAPI sprite IDs map to Pokémon, not arbitrary shared forms."""
    path = Path(__file__).resolve().parents[1] / 'data/pokeapi/pokemon_forms.csv'
    with path.open(encoding='utf-8', newline='') as source:
        rows = list(csv.DictReader(source))
    with (path.parent / 'pokemon.csv').open(encoding='utf-8', newline='') as source:
        species = {row['id']: int(row['species_id']) for row in csv.DictReader(source)}
    counts = {}
    for row in rows:
        counts[row['pokemon_id']] = counts.get(row['pokemon_id'], 0) + 1
    return {(species[row['pokemon_id']], row['identifier']): 'https://raw.githubusercontent.com/PokeAPI/sprites/c0542f7c51215d9672439012838c99f520596cbd/sprites/pokemon/' + row['pokemon_id'] + '.png'
            for row in rows if counts[row['pokemon_id']] == 1 and row['is_default'] == '1'}


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
                      dfj.status_presenca, dfj.pode_ser_registrada, dfj.status_tipos, dfj.fonte_tipos, dfj.data_verificacao_tipos, f.codigo_forma, e.nome_en,
                      dfj.fonte_url, dfj.data_verificacao,
                      f.fonte_url AS fonte_forma_url, f.data_verificacao AS data_verificacao_forma
               FROM ESPECIE e
               LEFT JOIN FORMA f ON f.id_especie = e.id_especie
               LEFT JOIN DADOS_FORMA_JOGO dfj ON dfj.id_forma = f.id_forma
               LEFT JOIN JOGO j ON j.id_jogo = dfj.id_jogo"""

    def listar(self, busca: str | None = None, *, tipo: int | None = None,
               geracao: int | None = None, jogo: int | None = None) -> list[PokemonCatalogo]:
        conditions, params = [], []
        if busca:
            term = busca.strip()
            conditions.append("(e.nome_pt LIKE ? OR e.nome_en LIKE ? OR f.nome_forma LIKE ? OR f.codigo_forma LIKE ? OR CAST(e.numero_nacional AS TEXT) = ?)")
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%", term])
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

    def listar_global(self, busca=None, **filtros):
        from dataclasses import replace
        # Filter contexts before grouping, so type and game refer to the SAME sheet.
        grouped = {}
        for item in self.listar(busca, **filtros):
            key = (item.id_especie, item.id_forma)
            grouped.setdefault(key, []).append(item)
        result = []
        for items in grouped.values():
            sheets = tuple(i.to_dict() | {"fichas": []} for i in items if i.id_dados_forma is not None)
            first = items[0]
            if len(items) > 1:
                first = replace(first, id_dados_forma=None, id_jogo=None, nome_jogo=None,
                                status_presenca=None, pode_ser_registrada=None, status_tipos=None, fonte_tipos=None, data_verificacao_tipos=None, tipos=())
            result.append(replace(first, fichas=sheets, fonte_url=first.fonte_forma_url,
                                  data_verificacao=first.data_verificacao_forma))
        return result

    def obter_forma(self, id_forma):
        row = get_db().execute("SELECT * FROM FORMA WHERE id_forma=?", (id_forma,)).fetchone()
        if not row:
            return None
        species = get_db().execute("SELECT * FROM ESPECIE WHERE id_especie=?", (row["id_especie"],)).fetchone()
        sheets = get_db().execute(self._SELECT + " WHERE f.id_forma=? ORDER BY j.id_jogo", (id_forma,))
        return dict(row) | {"especie": dict(species), "fichas": [self._row_to_model(r).to_dict() for r in sheets if r["id_dados_forma"] is not None]}

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
        return PokemonCatalogo(**dict(row), tipos=tuple(item["nome_tipo"] for item in tipos_rows),
                              imagem_url=_imagens_formas().get((row["numero_nacional"], row["codigo_forma"])))


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

    @staticmethod
    def _model(row):
        return PokemonColecao(**dict(row), valores=tuple(ValorDAO().listar("pokemon", row["id_pokemon_colecao"])))

    def atualizar_do_usuario(self, id_pokemon, id_usuario, dados):
        fields = ("id_dados_forma_atual", "id_mecanica", "id_jogo_origem", "id_dados_forma_origem",
                  "id_metodo_obtencao", "id_natureza", "id_habilidade_forma", "apelido", "nivel", "observacao")
        cursor = get_db().execute("UPDATE POKEMON_COLECAO SET " + ",".join(f"{f}=?" for f in fields)
            + " WHERE id_pokemon_colecao=? AND id_usuario=?", tuple(dados.get(f) for f in fields) + (id_pokemon, id_usuario))
        return cursor.rowcount > 0

    def listar_do_usuario(self, id_usuario: int) -> list[PokemonColecao]:
        rows = get_db().execute(
            self._SELECT + " WHERE pc.id_usuario = ? ORDER BY pc.id_pokemon_colecao DESC",
            (id_usuario,),
        ).fetchall()
        return [self._model(row) for row in rows]

    def obter_do_usuario(self, id_pokemon: int, id_usuario: int) -> PokemonColecao | None:
        row = get_db().execute(
            self._SELECT + " WHERE pc.id_pokemon_colecao = ? AND pc.id_usuario = ?",
            (id_pokemon, id_usuario),
        ).fetchone()
        return self._model(row) if row else None

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
        return PerfilAnalise(**dict(row), **self.relacionados(id_perfil)) if row else None

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

    def relacionados(self, id_perfil):
        db = get_db()
        return {"valores": tuple(ValorDAO().listar("perfil", id_perfil)),
                "naturezas": tuple(r[0] for r in db.execute("SELECT id_natureza FROM PERFIL_NATUREZA WHERE id_perfil=? ORDER BY id_natureza", (id_perfil,))),
                "habilidades": tuple(r[0] for r in db.execute("SELECT id_habilidade_forma FROM PERFIL_HABILIDADE WHERE id_perfil=? ORDER BY id_habilidade_forma", (id_perfil,)))}

    def listar_visiveis(self, id_usuario):
        ids = get_db().execute("SELECT id_perfil FROM PERFIL_ANALISE WHERE tipo_perfil='referencia_competitiva' OR id_usuario=? ORDER BY id_perfil", (id_usuario,))
        return [self.obter_visivel(r[0], id_usuario) for r in ids]

    def atualizar_personalizado(self, id_perfil, id_usuario, dados):
        fields = ("id_dados_forma", "id_mecanica", "id_regulamento", "nome_perfil", "descricao")
        return get_db().execute("UPDATE PERFIL_ANALISE SET " + ",".join(f"{f}=?" for f in fields)
            + " WHERE id_perfil=? AND id_usuario=? AND tipo_perfil='personalizado'",
            tuple(dados.get(f) for f in fields) + (id_perfil, id_usuario)).rowcount > 0

    def substituir_opcoes(self, id_perfil, naturezas, habilidades):
        db = get_db()
        for table, col, values in (("PERFIL_NATUREZA", "id_natureza", naturezas),
                                    ("PERFIL_HABILIDADE", "id_habilidade_forma", habilidades)):
            db.execute(f"DELETE FROM {table} WHERE id_perfil=?", (id_perfil,))
            db.executemany(f"INSERT INTO {table}(id_perfil,{col}) VALUES(?,?)", [(id_perfil, v) for v in values])

    def excluir_personalizado(self, id_perfil, id_usuario):
        with transaction(get_db()):
            return get_db().execute("DELETE FROM PERFIL_ANALISE WHERE id_perfil=? AND id_usuario=? AND tipo_perfil='personalizado'", (id_perfil, id_usuario)).rowcount > 0


class ValorDAO:
    # Identifiers only come from this fixed map; all supplied data is parameterized.
    CONFIG = {"pokemon": ("VALOR_ATRIBUTO_POKEMON", "id_pokemon_colecao", "valor"),
              "perfil": ("VALOR_PERFIL_ANALISE", "id_perfil", "valor_alvo")}

    def listar(self, tipo, id_dono):
        table, owner, value = self.CONFIG[tipo]
        return [dict(r) for r in get_db().execute(f"SELECT id_mecanica_sistema_atributo,id_atributo,estado,{value},motivo FROM {table} WHERE {owner}=? ORDER BY id_mecanica_sistema_atributo,id_atributo", (id_dono,))]

    def substituir(self, tipo, id_dono, valores):
        table, owner, value = self.CONFIG[tipo]
        db = get_db()
        # Caller owns the transaction, including parent and all related values.
        db.execute(f"DELETE FROM {table} WHERE {owner}=?", (id_dono,))
        db.executemany(f"INSERT INTO {table}({owner},id_mecanica_sistema_atributo,id_atributo,estado,{value},motivo) VALUES(?,?,?,?,?,?)",
            [(id_dono, v["id_mecanica_sistema_atributo"], v["id_atributo"], v["estado"], v.get(value), v.get("motivo")) for v in valores])


class ContextoDAO:
    def mecanica(self, id_mecanica):
        row = get_db().execute("SELECT * FROM MECANICA_JOGO WHERE id_mecanica=?", (id_mecanica,)).fetchone()
        if not row:
            return None
        systems = []
        for s in get_db().execute("SELECT m.*,s.codigo,s.nome FROM MECANICA_SISTEMA_ATRIBUTO m JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) WHERE id_mecanica=? ORDER BY id_mecanica_sistema_atributo", (id_mecanica,)):
            attrs = [dict(r) for r in get_db().execute("SELECT a.id_atributo,a.codigo,a.nome,m.fonte_url,m.data_verificacao,COALESCE(m.aplicabilidade,'nao_verificado') AS aplicabilidade FROM ATRIBUTO_BATALHA a LEFT JOIN MECANICA_ATRIBUTO m ON m.id_atributo=a.id_atributo AND m.id_mecanica_sistema_atributo=? ORDER BY a.id_atributo", (s["id_mecanica_sistema_atributo"],))]
            systems.append(dict(s) | {"atributos": attrs})
        return dict(row) | {"sistemas": systems}

    def opcoes(self):
        db = get_db()
        return {key: [dict(r) for r in db.execute(sql)] for key, sql in {
            "jogos": "SELECT * FROM JOGO ORDER BY id_jogo",
            "tipos": "SELECT * FROM TIPO ORDER BY id_tipo",
            "naturezas": "SELECT * FROM NATUREZA ORDER BY id_natureza",
            "metodos": "SELECT * FROM METODO_OBTENCAO ORDER BY id_metodo",
            "mecanicas": "SELECT * FROM MECANICA_JOGO ORDER BY id_mecanica"}.items()}

    def ficha(self, id_dados_forma):
        item = PokemonDAO().obter(id_dados_forma)
        if not item:
            return None
        db = get_db()
        raw = dict(db.execute("SELECT * FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?", (id_dados_forma,)).fetchone())
        raw.update(item.to_dict())
        raw["habilidades"] = [dict(r) for r in db.execute("SELECT h.*,a.nome,a.descricao FROM HABILIDADE_FORMA_JOGO h JOIN HABILIDADE a USING(id_habilidade) WHERE id_dados_forma=?", (id_dados_forma,))]
        raw["transformacoes"] = [dict(r) for r in db.execute("SELECT * FROM TRANSFORMACAO_FORMA WHERE id_dados_forma_origem=? OR id_dados_forma_destino=?", (id_dados_forma, id_dados_forma))]
        raw["mecanicas"] = [dict(r) for r in db.execute("SELECT * FROM MECANICA_JOGO WHERE id_jogo=?", (item.id_jogo,))]
        return raw


class RegulamentoDAO:
    def listar(self):
        return [dict(r) for r in get_db().execute("SELECT * FROM REGULAMENTO ORDER BY id_regulamento")]

    def obter(self, id_regulamento):
        r = get_db().execute("SELECT * FROM REGULAMENTO WHERE id_regulamento=?", (id_regulamento,)).fetchone()
        return dict(r) if r else None

    def elegibilidade(self, id_regulamento, id_dados_forma):
        rule = self.obter(id_regulamento)
        sheet = get_db().execute("SELECT id_jogo FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?", (id_dados_forma,)).fetchone()
        if not rule or not sheet:
            raise LookupError("Regulamento ou ficha não encontrado.")
        mechanic = ContextoDAO().mecanica(rule["id_mecanica"])
        if mechanic["id_jogo"] != sheet["id_jogo"]:
            raise ValueError("Regulamento e ficha pertencem a jogos incompatíveis.")
        row = get_db().execute("SELECT * FROM ELEGIBILIDADE_FORMA_REGULAMENTO WHERE id_regulamento=? AND id_dados_forma=?", (id_regulamento, id_dados_forma)).fetchone()
        evidence = dict(row) if row else {"id_regulamento": id_regulamento, "id_dados_forma": id_dados_forma,
            "status": "nao_verificado", "condicao": None, "fonte_url": None, "data_verificacao": None}
        return evidence | {"regulamento": rule, "escopo": "elegibilidade_da_forma", "legalidade_completa_verificada": False}
