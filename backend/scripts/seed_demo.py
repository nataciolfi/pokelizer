"""Insere um registro fictício de demonstração para testar a API localmente.

Este registro não pertence ao catálogo oficial e não deve ser usado em produção.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pokeanalyzer import create_app
from pokeanalyzer.db import get_db

app = create_app()

with app.app_context():
    db = get_db()
    db.execute(
        """INSERT OR IGNORE INTO ESPECIE
           (numero_nacional, nome_pt, nome_en, geracao_origem)
           VALUES (999999, 'Pokémon de demonstração', 'Demo Pokémon', NULL)"""
    )
    id_especie = db.execute(
        "SELECT id_especie FROM ESPECIE WHERE numero_nacional = 999999"
    ).fetchone()["id_especie"]

    db.execute(
        """INSERT OR IGNORE INTO FORMA
           (id_especie, codigo_forma, nome_forma, categoria, forma_padrao, descricao)
           VALUES (?, 'padrao-demo', 'Forma padrão (demo)', 'padrao', 1,
                   'Registro fictício para testar o backend local.')""",
        (id_especie,),
    )
    id_forma = db.execute(
        "SELECT id_forma FROM FORMA WHERE id_especie = ? AND codigo_forma = 'padrao-demo'",
        (id_especie,),
    ).fetchone()["id_forma"]

    db.execute(
        "INSERT OR IGNORE INTO JOGO (nome, categoria, plataforma) VALUES ('Jogo de demonstração', 'teste', 'local')"
    )
    id_jogo = db.execute(
        "SELECT id_jogo FROM JOGO WHERE nome = 'Jogo de demonstração'"
    ).fetchone()["id_jogo"]

    db.execute(
        """INSERT OR IGNORE INTO DADOS_FORMA_JOGO
           (id_forma, id_jogo, status_presenca, pode_ser_registrada)
           VALUES (?, ?, 'nativa', 'sim')""",
        (id_forma, id_jogo),
    )
    db.commit()
    id_dados = db.execute(
        "SELECT id_dados_forma FROM DADOS_FORMA_JOGO WHERE id_forma = ? AND id_jogo = ?",
        (id_forma, id_jogo),
    ).fetchone()["id_dados_forma"]
    print(f"Registro de demonstração preparado. id_dados_forma={id_dados}")
