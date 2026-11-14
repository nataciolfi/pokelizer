"""Adversarial physical model tests; all facts below are synthetic test fixtures."""
from pathlib import Path
import sqlite3

import pytest

SCHEMA = Path(__file__).resolve().parents[1] / 'schema.sql'
SOURCE = 'https://example.invalid/schema-test'
DATE = '2026-11-13'


@pytest.fixture
def db():
    db = sqlite3.connect(':memory:')
    db.executescript(SCHEMA.read_text())
    db.executescript(f"""
        INSERT INTO USUARIO VALUES(1,'schema_user','schema@example.invalid','{'x'*64}',CURRENT_TIMESTAMP);
        INSERT INTO ESPECIE(id_especie,numero_nacional,nome_pt) VALUES(1,900001,'Synthetic Alpha'),(2,900002,'Synthetic Beta');
        INSERT INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(1,1,'standard','Synthetic Standard',1),(2,2,'standard','Synthetic Standard',1),(3,1,'temporary','Synthetic Temporary',0);
        INSERT INTO JOGO(id_jogo,nome) VALUES(1,'Synthetic Game A'),(2,'Synthetic Game B');
        INSERT INTO DADOS_FORMA_JOGO(id_dados_forma,id_forma,id_jogo,status_presenca,pode_ser_registrada,fonte_url,data_verificacao) VALUES(1,1,1,'nativa','sim','{SOURCE}','{DATE}'),(2,2,1,'nativa','sim','{SOURCE}','{DATE}'),(3,1,2,'nativa','sim','{SOURCE}','{DATE}'),(4,3,1,'nativa','nao','{SOURCE}','{DATE}');
        INSERT INTO MECANICA_JOGO(id_mecanica,id_jogo,versao,usa_natureza,usa_habilidade,usa_nivel,nivel_minimo,nivel_maximo,fonte_url,data_verificacao) VALUES(1,1,'test-1','sim','sim','sim',1,20,'{SOURCE}','{DATE}'),(2,2,'test-1','nao','nao','nao',NULL,NULL,'{SOURCE}','{DATE}'),(3,1,'test-2','nao_verificado','nao_verificado','nao_verificado',NULL,NULL,NULL,NULL);
        INSERT INTO TIPO VALUES(1,'Synthetic Type A'),(2,'Synthetic Type B'),(3,'Synthetic Type C');
        INSERT INTO TIPO_FORMA_JOGO VALUES(1,1,1);
        UPDATE DADOS_FORMA_JOGO SET status_tipos='aplicavel' WHERE id_dados_forma=1;
        INSERT INTO HABILIDADE VALUES(1,'Synthetic Ability A',NULL),(2,'Synthetic Ability B',NULL);
        INSERT INTO HABILIDADE_FORMA_JOGO(id_habilidade_forma,id_dados_forma,id_habilidade,slot,fonte_url,data_verificacao) VALUES(1,1,1,'normal','{SOURCE}','{DATE}'),(2,2,2,'normal','{SOURCE}','{DATE}');
        INSERT INTO METODO_OBTENCAO VALUES(1,'Synthetic Original Acquisition',NULL),(2,'Synthetic Transfer',NULL);
        INSERT INTO METODO_FORMA_JOGO VALUES(3,2,NULL,'{SOURCE}','{DATE}');
        INSERT INTO ATRIBUTO_BATALHA VALUES(1,'TEST_A','Synthetic Attribute A'),(2,'TEST_B','Synthetic Attribute B');
        INSERT INTO NATUREZA(id_natureza,nome) VALUES(1,'Synthetic Nature');
        INSERT INTO SISTEMA_ATRIBUTO VALUES(1,'TEST_SYSTEM','Synthetic Attribute System',NULL);
        INSERT INTO MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo,id_mecanica,id_sistema_atributo,aplicabilidade,unidade,valor_minimo,valor_maximo_atributo,valor_maximo_total,limite_total_status,fonte_url,data_verificacao) VALUES(1,1,1,'aplicavel','test-units',0,10,15,'confirmado','{SOURCE}','{DATE}'),(2,2,1,'nao_aplicavel',NULL,NULL,NULL,NULL,'nao_verificado','{SOURCE}','{DATE}'),(3,3,1,'nao_verificado',NULL,NULL,NULL,NULL,'nao_verificado',NULL,NULL);
        INSERT INTO MECANICA_ATRIBUTO VALUES(1,1,'aplicavel','{SOURCE}','{DATE}'),(1,2,'aplicavel','{SOURCE}','{DATE}'),(2,1,'nao_aplicavel','{SOURCE}','{DATE}');
        INSERT INTO POKEMON_COLECAO(id_pokemon_colecao,id_usuario,id_dados_forma_atual,id_mecanica,nivel,id_natureza,id_habilidade_forma) VALUES(1,1,1,1,10,1,1);
        INSERT INTO REGULAMENTO(id_regulamento,id_mecanica,codigo,versao,nome,formato,temporada,fonte_url,data_verificacao) VALUES(1,1,'test','1','Synthetic Rules','test','test','{SOURCE}','{DATE}'),(2,2,'test','1','Synthetic Rules','test','test','{SOURCE}','{DATE}');
        INSERT INTO PERFIL_ANALISE(id_perfil,id_dados_forma,id_mecanica,id_usuario,nome_perfil,tipo_perfil) VALUES(1,1,1,1,'Synthetic Custom','personalizado');
    """)
    yield db
    db.close()


def reject(db, sql, args=()):
    """A rejected write must preserve the database; test each violation independently."""
    db.execute('SAVEPOINT rejection')
    try:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(sql, args)
    finally:
        db.execute('ROLLBACK TO rejection')
        db.execute('RELEASE rejection')


def test_complete_species_requires_one_standard_and_cannot_lose_it(db):
    reject(db,"UPDATE ESPECIE SET status_catalogo='completo',fonte_url=?,data_verificacao=? WHERE id_especie=1",(SOURCE,'2026-02-30'))
    db.execute("UPDATE ESPECIE SET status_catalogo='completo',fonte_url=?,data_verificacao=? WHERE id_especie=1",(SOURCE,DATE))
    reject(db,"INSERT INTO FORMA(id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(1,'other','Other',1)")
    reject(db,'DELETE FROM FORMA WHERE id_forma=1')
    reject(db,'UPDATE FORMA SET forma_padrao=0 WHERE id_forma=1')
    db.execute("INSERT INTO ESPECIE(id_especie,numero_nacional,nome_pt) VALUES(3,900003,'Synthetic No Form')")
    reject(db,"UPDATE ESPECIE SET status_catalogo='completo',fonte_url=?,data_verificacao=? WHERE id_especie=3",(SOURCE,DATE))
    assert db.execute('SELECT count(*) FROM DADOS_FORMA_JOGO WHERE id_forma=3').fetchone()[0] == 1
    # Species without a game context are independently catalogable.
    db.execute("INSERT INTO FORMA(id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(3,'standard','Synthetic Standard',1)")
    db.execute("UPDATE ESPECIE SET status_catalogo='completo',fonte_url=?,data_verificacao=? WHERE id_especie=3",(SOURCE,DATE))


def test_identity_uniqueness_strict_values_and_foreign_keys(db):
    assert db.execute('PRAGMA foreign_keys').fetchone()[0] == 1
    reject(db,"INSERT INTO ESPECIE(numero_nacional,nome_pt) VALUES(900001,'Duplicate')")
    reject(db,"INSERT INTO FORMA(id_especie,codigo_forma,nome_forma) VALUES(999,'bad','Bad')")
    reject(db,"INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo) VALUES(1,1)")
    reject(db,"INSERT INTO ESPECIE(numero_nacional,nome_pt) VALUES('not-an-integer','Bad')")
    reject(db,'UPDATE POKEMON_COLECAO SET nivel=1.25 WHERE id_pokemon_colecao=1')
    reject(db,'UPDATE FORMA SET id_especie=2 WHERE id_forma=3')
    reject(db,"UPDATE SISTEMA_ATRIBUTO SET codigo='REPURPOSED' WHERE id_sistema_atributo=1")


def test_type_slots_coverage_insert_update_delete(db):
    reject(db,'INSERT INTO TIPO_FORMA_JOGO VALUES(1,2,1)')
    reject(db,'INSERT INTO TIPO_FORMA_JOGO VALUES(1,1,2)')
    db.execute('INSERT INTO TIPO_FORMA_JOGO VALUES(1,2,2)')
    reject(db,'INSERT INTO TIPO_FORMA_JOGO VALUES(1,3,3)')
    reject(db,'DELETE FROM TIPO_FORMA_JOGO WHERE id_dados_forma=1 AND posicao=1')
    reject(db,'UPDATE TIPO_FORMA_JOGO SET id_dados_forma=2 WHERE id_dados_forma=1 AND posicao=1')
    reject(db,"UPDATE DADOS_FORMA_JOGO SET status_tipos='aplicavel' WHERE id_dados_forma=2")
    reject(db,"UPDATE DADOS_FORMA_JOGO SET status_tipos='nao_aplicavel' WHERE id_dados_forma=1")
    db.execute('DELETE FROM TIPO_FORMA_JOGO WHERE id_dados_forma=1 AND posicao=2')


def test_specimen_ability_mechanics_level_and_registrability(db):
    reject(db,'UPDATE POKEMON_COLECAO SET id_habilidade_forma=2 WHERE id_pokemon_colecao=1')
    reject(db,'UPDATE POKEMON_COLECAO SET id_mecanica=2 WHERE id_pokemon_colecao=1')
    reject(db,'UPDATE POKEMON_COLECAO SET nivel=21 WHERE id_pokemon_colecao=1')
    reject(db,'UPDATE POKEMON_COLECAO SET id_mecanica=3 WHERE id_pokemon_colecao=1')
    reject(db,'INSERT INTO POKEMON_COLECAO(id_usuario,id_dados_forma_atual) VALUES(1,4)')
    reject(db,"UPDATE DADOS_FORMA_JOGO SET pode_ser_registrada='nao' WHERE id_dados_forma=1")
    reject(db,"UPDATE MECANICA_JOGO SET nivel_maximo=9 WHERE id_mecanica=1")
    reject(db,'UPDATE HABILIDADE_FORMA_JOGO SET id_dados_forma=2 WHERE id_habilidade_forma=1')
    reject(db,"UPDATE NATUREZA SET estado_efeito='neutro',fonte_url=?,data_verificacao=? WHERE id_natureza=1",(SOURCE,DATE))


def test_transfer_preserves_actual_origin_acquisition_not_current_availability(db):
    # Method 1 is NOT available in context 3. It can still describe original acquisition.
    db.execute('INSERT INTO POKEMON_COLECAO(id_usuario,id_dados_forma_atual,id_jogo_origem,id_dados_forma_origem,id_metodo_obtencao) VALUES(1,3,1,1,1)')
    reject(db,'UPDATE POKEMON_COLECAO SET id_dados_forma_origem=3 WHERE id_pokemon_colecao=2')
    assert db.execute('SELECT id_metodo_obtencao FROM POKEMON_COLECAO WHERE id_pokemon_colecao=2').fetchone()[0] == 1


def test_profile_owner_context_and_recommended_options(db):
    reject(db,"INSERT INTO PERFIL_ANALISE(id_dados_forma,id_mecanica,nome_perfil,tipo_perfil) VALUES(1,1,'Ownerless','personalizado')")
    reject(db,"INSERT INTO PERFIL_ANALISE(id_dados_forma,id_mecanica,id_usuario,nome_perfil,tipo_perfil) VALUES(1,2,1,'Wrong Game','personalizado')")
    reject(db,'UPDATE PERFIL_ANALISE SET id_regulamento=2 WHERE id_perfil=1')
    reject(db,"INSERT INTO PERFIL_ANALISE(id_dados_forma,id_mecanica,nome_perfil,tipo_perfil) VALUES(1,1,'Unsourced','referencia_competitiva')")
    db.execute('INSERT INTO PERFIL_NATUREZA VALUES(1,1)')
    db.execute('INSERT INTO PERFIL_HABILIDADE VALUES(1,1)')
    reject(db,'UPDATE PERFIL_HABILIDADE SET id_habilidade_forma=2 WHERE id_perfil=1')
    reject(db,'UPDATE PERFIL_ANALISE SET id_dados_forma=2 WHERE id_perfil=1')
    reject(db,"UPDATE MECANICA_JOGO SET usa_natureza='nao' WHERE id_mecanica=1")


@pytest.mark.parametrize('table,owner,value,pk',[
    ('VALOR_ATRIBUTO_POKEMON','id_pokemon_colecao','valor','id_valor_atributo'),
    ('VALOR_PERFIL_ANALISE','id_perfil','valor_alvo','id_valor_perfil'),
])
def test_numeric_applicability_limits_totals_unknown_states_and_updates(db,table,owner,value,pk):
    statement=f'INSERT INTO {table}({owner},id_mecanica_sistema_atributo,id_atributo,{value}) VALUES(1,?,?,?)'
    reject(db,statement,(1,1,11))
    reject(db,statement,(1,1,-1))
    reject(db,statement,(2,1,1))
    db.execute(statement,(1,1,10))
    reject(db,statement,(1,2,6))
    db.execute(statement,(1,2,5))
    reject(db,f'UPDATE {table} SET {value}=6 WHERE {owner}=1 AND id_atributo=2')
    # Updating an existing row excludes its old value, and changing owners is revalidated.
    db.execute(f'UPDATE {table} SET {value}=4 WHERE {owner}=1 AND id_atributo=2')
    reject(db,"UPDATE MECANICA_SISTEMA_ATRIBUTO SET valor_maximo_total=13 WHERE id_mecanica_sistema_atributo=1")
    reject(db,"UPDATE MECANICA_SISTEMA_ATRIBUTO SET unidade='different-scale' WHERE id_mecanica_sistema_atributo=1")
    reject(db,"UPDATE MECANICA_ATRIBUTO SET aplicabilidade='nao_aplicavel' WHERE id_mecanica_sistema_atributo=1 AND id_atributo=1")
    reject(db,'DELETE FROM MECANICA_ATRIBUTO WHERE id_mecanica_sistema_atributo=1 AND id_atributo=1')
    reject(db,f"UPDATE {table} SET estado='desconhecido' WHERE {owner}=1 AND id_atributo=1")
    db.execute(f"UPDATE {table} SET estado='desconhecido',{value}=NULL WHERE {owner}=1 AND id_atributo=1")
    row=db.execute(f'SELECT estado,{value} FROM {table} WHERE {owner}=1 AND id_atributo=1').fetchone()
    assert row == ('desconhecido',None)
    reject(db,f"UPDATE {table} SET estado='nao_aplicavel',{value}=NULL WHERE {owner}=1 AND id_atributo=1")


def test_unknown_limits_block_known_values_but_retain_explicit_unknown(db):
    db.execute('INSERT INTO POKEMON_COLECAO(id_usuario,id_dados_forma_atual,id_mecanica) VALUES(1,1,3)')
    reject(db,'INSERT INTO VALOR_ATRIBUTO_POKEMON(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo,valor) VALUES(2,3,1,0)')
    db.execute("INSERT INTO VALOR_ATRIBUTO_POKEMON(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo,estado) VALUES(2,3,1,'desconhecido')")
    reject(db,'UPDATE POKEMON_COLECAO SET id_mecanica=1 WHERE id_pokemon_colecao=2')
    db.execute('INSERT INTO POKEMON_COLECAO(id_usuario,id_dados_forma_atual,id_mecanica) VALUES(1,3,2)')
    db.execute("INSERT INTO VALOR_ATRIBUTO_POKEMON(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo,estado) VALUES(3,2,1,'nao_aplicavel')")


def test_eligibility_unique_sourced_compatible_and_not_full_legality(db):
    insert='INSERT INTO ELEGIBILIDADE_FORMA_REGULAMENTO(id_regulamento,id_dados_forma,status,fonte_url,data_verificacao) VALUES(?,?,?,?,?)'
    reject(db,insert,(1,3,'permitido',SOURCE,DATE))
    reject(db,insert,(1,1,'permitido',None,None))
    reject(db,insert,(1,1,'condicional',SOURCE,DATE))
    db.execute(insert,(1,1,'permitido',SOURCE,DATE))
    reject(db,insert,(1,1,'proibido',SOURCE,DATE))
    reject(db,"UPDATE REGULAMENTO SET id_mecanica=2 WHERE id_regulamento=1")
    reject(db,'UPDATE DADOS_FORMA_JOGO SET id_jogo=2 WHERE id_dados_forma=1')
    assert db.execute('SELECT count(*) FROM ELEGIBILIDADE_FORMA_REGULAMENTO WHERE id_dados_forma=2').fetchone()[0] == 0


def test_transformation_context_and_reverse_edits(db):
    insert='INSERT INTO TRANSFORMACAO_FORMA(id_dados_forma_origem,id_dados_forma_destino,tipo_transformacao,temporaria,condicao,fonte_url,data_verificacao) VALUES(?,?,?,?,?,?,?)'
    reject(db,insert,(1,3,'synthetic',1,'synthetic condition',SOURCE,DATE))
    db.execute(insert,(1,4,'synthetic',1,'synthetic condition',SOURCE,DATE))
    reject(db,'UPDATE TRANSFORMACAO_FORMA SET id_dados_forma_destino=3 WHERE id_transformacao=1')
    reject(db,'UPDATE DADOS_FORMA_JOGO SET id_jogo=2 WHERE id_dados_forma=4')
    assert db.execute('SELECT count(*) FROM POKEMON_COLECAO').fetchone()[0] == 1


def test_deletion_actions_preserve_catalog_and_remove_private_dependents(db):
    db.execute('INSERT INTO VALOR_ATRIBUTO_POKEMON(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo,valor) VALUES(1,1,1,10)')
    db.execute('INSERT INTO PERFIL_NATUREZA VALUES(1,1)')
    reject(db,'DELETE FROM JOGO WHERE id_jogo=1')
    reject(db,'DELETE FROM DADOS_FORMA_JOGO WHERE id_dados_forma=1')
    reject(db,'DELETE FROM HABILIDADE_FORMA_JOGO WHERE id_habilidade_forma=1')
    db.execute('DELETE FROM USUARIO WHERE id_usuario=1')
    for table in ('POKEMON_COLECAO','VALOR_ATRIBUTO_POKEMON','PERFIL_ANALISE','PERFIL_NATUREZA'):
        assert db.execute(f'SELECT count(*) FROM {table}').fetchone()[0] == 0
    assert db.execute('SELECT count(*) FROM ESPECIE').fetchone()[0] == 2
    assert db.execute('PRAGMA foreign_key_check').fetchall() == []
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'


def test_physical_model_contains_ordered_migrations():
    first=(SCHEMA.parent/'migrations'/'001_stage1.sql').read_bytes()
    second=(SCHEMA.parent/'migrations'/'002_catalog_evidence.sql').read_bytes()
    assert SCHEMA.read_bytes() == first + b'\n' + second


def test_replace_cannot_bypass_standard_type_or_applicability_invariants(db):
    # Guard structural integrity even for tools that disable recursive DELETE triggers.
    db.execute('PRAGMA recursive_triggers=OFF')
    db.execute("INSERT INTO ESPECIE(id_especie,numero_nacional,nome_pt) VALUES(3,900003,'Synthetic Replace Target')")
    db.execute("INSERT INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(5,3,'standard','Synthetic Standard',1)")
    db.execute("UPDATE ESPECIE SET status_catalogo='completo',fonte_url=?,data_verificacao=? WHERE id_especie=3",(SOURCE,DATE))
    reject(db,"INSERT OR REPLACE INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(5,3,'standard','Replaced',0)")
    reject(db,"INSERT OR REPLACE INTO FORMA(id_forma,id_especie,codigo_forma,nome_forma,forma_padrao) VALUES(6,3,'standard','Replaced',0)")
    reject(db,'INSERT OR REPLACE INTO TIPO_FORMA_JOGO VALUES(1,1,2)')
    db.execute('INSERT INTO VALOR_ATRIBUTO_POKEMON(id_pokemon_colecao,id_mecanica_sistema_atributo,id_atributo,valor) VALUES(1,1,1,10)')
    reject(db,"INSERT OR REPLACE INTO MECANICA_ATRIBUTO VALUES(1,1,'nao_aplicavel',?,?)",(SOURCE,DATE))


def test_generator_check_detects_source_drift_without_rewriting(tmp_path):
    import shutil
    import subprocess
    import sys
    backend=tmp_path/'backend'
    shutil.copytree(SCHEMA.parent/'tools',backend/'tools')
    (backend/'migrations').mkdir()
    shutil.copyfile(SCHEMA,backend/'schema.sql')
    shutil.copyfile(SCHEMA.parent/'migrations'/'001_stage1.sql',backend/'migrations'/'001_stage1.sql')
    shutil.copyfile(SCHEMA.parent/'migrations'/'002_catalog_evidence.sql',backend/'migrations'/'002_catalog_evidence.sql')
    command=[sys.executable,str(backend/'tools'/'build_schema.py'),'--check']
    assert subprocess.run(command,capture_output=True).returncode == 0
    with (backend/'tools'/'schema_base.sql').open('a') as source:
        source.write('\n-- Synthetic drift for check test\n')
    before=(backend/'schema.sql').read_bytes()
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode != 0
    assert 'differs from source' in result.stderr
    assert (backend/'schema.sql').read_bytes() == before
