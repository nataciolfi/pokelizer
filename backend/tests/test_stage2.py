"""Behavioral regressions for Stage 2; all catalog facts are explicitly synthetic."""
import pytest
from test_api import app, client, create_user, get_csrf
from pokeanalyzer.db import get_db


@pytest.fixture()
def rules(app):
    with app.app_context():
        db = get_db()
        db.executescript("""
        INSERT INTO ATRIBUTO_BATALHA VALUES(1,'fixture-a','FIXTURE A'),(2,'fixture-b','FIXTURE B');
        INSERT INTO SISTEMA_ATRIBUTO VALUES(1,'fixture-values','FIXTURE values',NULL),(2,'fixture-na','FIXTURE N/A',NULL),(3,'fixture-unknown','FIXTURE unknown',NULL);
        INSERT INTO MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo,id_mecanica,id_sistema_atributo,aplicabilidade,valor_minimo,valor_maximo_atributo,valor_maximo_total,limite_total_status,fonte_url,data_verificacao)
        VALUES(1,1,1,'aplicavel',0,10,12,'confirmado','https://example.invalid/fixture','2026-11-13'),
              (2,1,2,'nao_aplicavel',NULL,NULL,NULL,'nao_verificado','https://example.invalid/fixture','2026-11-13'),
              (3,1,3,'nao_verificado',NULL,NULL,NULL,'nao_verificado',NULL,NULL);
        INSERT INTO MECANICA_ATRIBUTO VALUES(1,1,'aplicavel','https://example.invalid/fixture','2026-11-13'),(1,2,'aplicavel','https://example.invalid/fixture','2026-11-13'),(2,1,'nao_aplicavel','https://example.invalid/fixture','2026-11-13'),(3,1,'nao_verificado',NULL,NULL);
        INSERT INTO REGULAMENTO(id_regulamento,id_mecanica,codigo,versao,nome,formato,temporada,fonte_url,data_verificacao)
        VALUES(1,1,'fixture','fixture-v1','FIXTURE rule','fixture','fixture','https://example.invalid/fixture','2026-11-13');
        INSERT INTO NATUREZA(id_natureza,nome) VALUES(1,'FIXTURE nature');
        """)
        db.commit()


def write(client, method, url, body):
    return getattr(client, method)(url, json=body, headers={"X-CSRF-Token": get_csrf(client)})


def value(number=0, attr=1, system=1, field='valor', state='conhecido'):
    return {"id_mecanica_sistema_atributo": system, "id_atributo": attr, "estado": state, field: number}


def specimen(client, values=None):
    return write(client, 'post', '/api/colecao', {"id_dados_forma_atual": 1, "id_mecanica": 1, "valores": values or []})


def profile(client, values=None, **extra):
    return write(client, 'post', '/api/perfis', {"id_dados_forma": 1, "id_mecanica": 1, "nome_perfil": "FIXTURE target", "valores": values or [], **extra})


def test_values_and_collection_edit_delete_are_atomic(client, rules):
    create_user(client)
    created = specimen(client, [value(0), value(5, attr=2)])
    assert created.status_code == 201
    pid = created.json['id_pokemon_colecao']
    assert created.json['valores'][0]['valor'] == 0
    changed = write(client, 'patch', f'/api/colecao/{pid}', {"apelido": "FIXTURE changed", "valores": [value(7), value(5, attr=2)]})
    assert changed.status_code == 200
    assert changed.json['apelido'] == 'FIXTURE changed'
    # Both individually valid, invalid combined total; parent and first insert roll back.
    bad = write(client, 'patch', f'/api/colecao/{pid}', {"apelido": "must rollback", "valores": [value(8), value(5, attr=2)]})
    assert bad.status_code == 400
    persisted = client.get(f'/api/colecao/{pid}').json
    assert persisted == changed.json
    assert write(client, 'delete', f'/api/colecao/{pid}', {}).status_code == 200
    assert client.get(f'/api/colecao/{pid}').status_code == 404


def test_invalid_child_rolls_back_parent_creation(client, rules, app):
    create_user(client)
    assert specimen(client, [value(11)]).status_code == 400
    assert client.get('/api/colecao').json['total'] == 0
    assert profile(client, [value(11, field='valor_alvo')]).status_code == 400
    assert client.get('/api/perfis').json['total'] == 0
    with app.app_context():
        assert not get_db().execute('PRAGMA foreign_key_check').fetchall()


@pytest.mark.parametrize('body', [None, [], {'oops': 1}, {'valores': None}, {'valores': [value(True)]}, {'valores': [value(1.5)]}, {'valores': [value(1), value(2)]}, {'valores': [value(1) | {'typo': 1}]}])
def test_reject_invalid_payload_without_success(client, rules, body):
    create_user(client)
    if isinstance(body, dict):
        body = {'id_dados_forma_atual': 1, 'id_mecanica': 1, **body}
    assert write(client, 'post', '/api/colecao', body).status_code == 400
    assert client.get('/api/colecao').json['total'] == 0


def test_unknown_fields_on_auth_and_filters(client):
    assert write(client, 'post', '/api/auth/cadastro', {'nome_usuario': 'fixture', 'email': 'f@example.invalid', 'senha': 'fixture-password', 'admin': True}).status_code == 400
    assert client.get('/api/pokemon?unknown=x').status_code == 400
    assert client.get('/api/pokemon?tipo=1&tipo=2').status_code == 400


def test_profile_crud_preferences_and_private_access(client, app, rules):
    create_user(client)
    p = profile(client, [value(0, field='valor_alvo')], naturezas=[1], habilidades=[1])
    assert p.status_code == 201
    pid = p.json['id_perfil']
    edited = write(client, 'patch', f'/api/perfis/{pid}', {'descricao': 'FIXTURE description', 'valores': [value(5, field='valor_alvo')]})
    assert edited.status_code == 200
    assert edited.json['naturezas'] == [1]
    assert edited.json['descricao'] == 'FIXTURE description'
    bad = write(client, 'patch', f'/api/perfis/{pid}', {'nome_perfil': 'rolled back', 'habilidades': [999]})
    assert bad.status_code == 400
    assert client.get(f'/api/perfis/{pid}').json == edited.json
    s = specimen(client).json['id_pokemon_colecao']
    other = app.test_client()
    create_user(other, 'fixture_other', 'other@example.invalid')
    for base, ident in [('perfis', pid), ('colecao', s)]:
        assert other.get(f'/api/{base}/{ident}').status_code == 404
        assert write(other, 'patch', f'/api/{base}/{ident}', {'apelido' if base=='colecao' else 'nome_perfil': 'invasion'}).status_code == 404
        assert write(other, 'delete', f'/api/{base}/{ident}', {}).status_code == 404
    assert other.get('/api/perfis').json['total'] == 0
    assert write(other, 'post', '/api/analises', {'id_perfil': pid, 'id_pokemon_colecao': s}).status_code == 404
    assert write(client, 'delete', f'/api/perfis/{pid}', {}).status_code == 200
    assert client.get(f'/api/perfis/{pid}').status_code == 404


def test_analysis_zero_missing_not_applicable_unknown_and_lower_target(client, rules):
    create_user(client)
    s = specimen(client, [value(0), value(None, system=2, state='nao_aplicavel')]).json
    p = profile(client, [value(2, field='valor_alvo'), value(0, attr=2, field='valor_alvo')], id_regulamento=1, naturezas=[1]).json
    result = write(client, 'post', '/api/analises', {'id_pokemon_colecao': s['id_pokemon_colecao'], 'id_perfil': p['id_perfil']})
    assert result.status_code == 200
    rows = result.json['campos']
    assert rows[0]['estado'] == 'abaixo' and rows[0]['diferenca'] == -2 and rows[0]['real'] == 0
    assert rows[1]['estado'] == 'sem_dado' and rows[1]['real'] is None and rows[1]['alvo'] == 0
    assert rows[2]['estado'] == 'nao_aplicavel'
    assert rows[4]['estado'] == 'nao_verificado'
    assert result.json['preferencias'][0]['estado'] == 'sem_dado'
    assert result.json['elegibilidade']['status'] == 'nao_verificado'
    assert result.json['legalidade_completa_verificada'] is False
    assert 'nota' not in result.json
    write(client, 'patch', f"/api/colecao/{s['id_pokemon_colecao']}", {'valores': [value(5)]})
    result = write(client, 'post', '/api/analises', {'id_pokemon_colecao': s['id_pokemon_colecao'], 'id_perfil': p['id_perfil']})
    assert result.json['campos'][0]['estado'] == 'acima'


def test_incompatible_mechanics_and_explicit_context_transition(client, rules, app):
    create_user(client)
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO MECANICA_JOGO(id_mecanica,id_jogo,versao) VALUES(2,1,'FIXTURE v2')")
        db.commit()
    s=specimen(client,[value(0)]).json
    p=profile(client, id_mecanica=2).json
    assert write(client,'post','/api/analises', {'id_pokemon_colecao':s['id_pokemon_colecao'],'id_perfil':p['id_perfil']}).status_code == 400
    path=f"/api/colecao/{s['id_pokemon_colecao']}"
    assert write(client,'patch',path,{'id_mecanica':2}).status_code == 400
    ok=write(client,'patch',path,{'id_mecanica':2,'valores':[]})
    assert ok.status_code == 200 and ok.json['valores'] == []
    assert write(client,'post','/api/analises', {'id_pokemon_colecao':s['id_pokemon_colecao'],'id_perfil':p['id_perfil']}).status_code == 200


def test_catalog_code_number_name_single_identity_and_same_sheet_filters(client, app):
    with app.app_context():
        db=get_db()
        db.executescript("INSERT INTO JOGO(id_jogo,nome) VALUES(2,'FIXTURE other'); INSERT INTO DADOS_FORMA_JOGO(id_dados_forma,id_forma,id_jogo) VALUES(2,1,2);")
    for query in ['fixture-standard','99901','species A']:
        result=client.get('/api/pokemon',query_string={'busca':query}).json
        assert result['total'] == 1
        assert len(result['itens'][0]['fichas']) == 2
        assert result['itens'][0]['codigo_forma'] == 'fixture-standard'
        assert result['itens'][0]['id_dados_forma'] is None
    assert client.get('/api/pokemon?jogo=2&tipo=1').json['total'] == 0
    assert client.get('/api/pokemon?jogo=1&tipo=1').json['total'] == 1
    assert len(client.get('/api/formas/1').json['fichas']) == 2
    assert client.get('/api/pokemon/1').json['habilidades'][0]['id_habilidade_forma'] == 1


def test_regulation_evidence_and_cross_game_rejection(client, rules, app):
    with app.app_context():
        db=get_db()
        db.executescript("INSERT INTO ELEGIBILIDADE_FORMA_REGULAMENTO(id_regulamento,id_dados_forma,status,fonte_url,data_verificacao) VALUES(1,1,'permitido','https://example.invalid/evidence','2026-11-13'); INSERT INTO JOGO(id_jogo,nome) VALUES(2,'FIXTURE B'); INSERT INTO DADOS_FORMA_JOGO(id_dados_forma,id_forma,id_jogo) VALUES(2,1,2);")
    item=client.get('/api/regulamentos/1/formas/1').json
    assert item['status']=='permitido' and item['fonte_url']=='https://example.invalid/evidence'
    assert item['legalidade_completa_verificada'] is False
    assert client.get('/api/regulamentos/1/formas/2').status_code==400
    assert client.get('/api/regulamentos/999/formas/1').status_code==404


@pytest.mark.parametrize('body',[{'valores':None},{'naturezas':None},{'habilidades':None},{'valores':{}},{'nome_perfil':True}])
def test_profile_edit_rejects_malformed_lists(client, rules, body):
    create_user(client)
    p=profile(client).json
    assert write(client,'patch',f"/api/perfis/{p['id_perfil']}",body).status_code==400
    assert client.get(f"/api/perfis/{p['id_perfil']}").json == p


def test_unknown_value_without_attribute_rule_is_still_reported(client, rules, app):
    create_user(client)
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO ATRIBUTO_BATALHA VALUES(3,'fixture-c','FIXTURE no rule')")
        db.commit()
    s=specimen(client,[value(None,attr=3,state='desconhecido')]).json
    p=profile(client,[value(None,attr=3,state='desconhecido',field='valor_alvo')]).json
    result=write(client,'post','/api/analises',{'id_pokemon_colecao':s['id_pokemon_colecao'],'id_perfil':p['id_perfil']})
    row=next(r for r in result.json['campos'] if r['id_atributo']==3)
    assert row['estado']=='nao_verificado' and row['estado_real']=='desconhecido'


def test_application_serves_integrated_interface_and_coverage(client):
    page=client.get('/')
    assert page.status_code==200
    assert b'<html lang="pt-BR">' in page.data
    assert b'/static/app.js' in page.data and b'/static/app.css' in page.data
    assert client.get('/static/app.js').status_code==200
    assert client.get('/static/app.css').status_code==200
    coverage=client.get('/api/catalogo/cobertura')
    assert coverage.status_code==200
    assert coverage.json['contagens_banco']['ESPECIE']==1
    assert coverage.json['cobertura_snapshot']['especies_importadas']==0


def test_global_and_game_sheet_evidence_remain_distinct(client, app):
    with app.app_context():
        db=get_db()
        db.execute("UPDATE FORMA SET fonte_url='https://example.invalid/global-form',data_verificacao='2026-11-12' WHERE id_forma=1")
        db.commit()
    sheet=client.get('/api/pokemon/1').json
    assert sheet['fonte_url']=='https://example.invalid/fixture'
    assert sheet['data_verificacao']=='2026-11-13'
    assert sheet['fonte_forma_url']=='https://example.invalid/global-form'
    global_item=client.get('/api/pokemon').json['itens'][0]
    assert global_item['fonte_url']=='https://example.invalid/global-form'
    assert global_item['fichas'][0]['fonte_url']=='https://example.invalid/fixture'
    detail=client.get('/api/formas/1').json
    assert detail['fonte_url']=='https://example.invalid/global-form'
    assert detail['fichas'][0]['fonte_url']=='https://example.invalid/fixture'


def test_non_ascii_invalid_csrf_is_rejected_without_server_error(client):
    create_user(client)
    response=client.post('/api/colecao',json={'id_dados_forma_atual':1},headers={'X-CSRF-Token':'inválido'})
    assert response.status_code==403
