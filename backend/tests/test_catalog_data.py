from test_api import app
from pokeanalyzer.catalog_data import importar_catalogo, ler_snapshot
from pokeanalyzer.db import get_db
import pytest


def test_real_snapshot_repeatable_preserves_private_data_and_reports_unknowns(app):
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO USUARIO(nome_usuario,email,senha_hash) VALUES('FIXTURE preserved','fixture@example.invalid',?)",('x'*64,))
        db.commit()
        first=importar_catalogo()
        second=importar_catalogo()
        assert first==second
        c=first['cobertura_snapshot']
        assert c['especies_importadas']==c['especies_fonte']>=1025
        assert c['formas_importadas']==c['formas_fonte']>c['especies_fonte']
        assert db.execute('SELECT nome_usuario FROM USUARIO').fetchone()[0]=='FIXTURE preserved'
        assert db.execute("SELECT count(*) FROM ESPECIE WHERE nome_en='Pikachu'").fetchone()[0]==1
        assert db.execute('SELECT count(*) FROM DADOS_FORMA_JOGO').fetchone()[0]==1 # only fixture, no invented game data
        assert db.execute("SELECT count(*) FROM FORMA WHERE fonte_url=? AND forma_padrao=0 AND categoria!='nao_verificada'",(first['fonte_url'],)).fetchone()[0]==0
        assert not db.execute('PRAGMA foreign_key_check').fetchall()


def test_conflicting_data_is_not_overwritten(app):
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO ESPECIE(numero_nacional,nome_pt) VALUES(25,'FIXTURE conflict')")
        db.commit()
        before=db.execute('SELECT count(*) FROM ESPECIE').fetchone()[0]
        with pytest.raises(ValueError,match='Conflito'):
            importar_catalogo()
        assert db.execute('SELECT count(*) FROM ESPECIE').fetchone()[0]==before
        assert db.execute('SELECT nome_pt FROM ESPECIE WHERE numero_nacional=25').fetchone()[0]=='FIXTURE conflict'


def test_curated_form_category_is_not_silently_replaced(app):
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        form=db.execute("SELECT id_forma FROM FORMA WHERE fonte_url=? AND forma_padrao=0 LIMIT 1",(report['fonte_url'],)).fetchone()[0]
        db.execute("UPDATE FORMA SET categoria='FIXTURE curated category' WHERE id_forma=?",(form,))
        db.commit()
        with pytest.raises(ValueError,match='Conflito em forma'):
            importar_catalogo()
        assert db.execute('SELECT categoria FROM FORMA WHERE id_forma=?',(form,)).fetchone()[0]=='FIXTURE curated category'
