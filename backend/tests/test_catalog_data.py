from test_api import app, client
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
        assert first['fichas_encontro_documentado'] >= 5000
        assert first['fichas_outras_fontes_preservadas'] == 1
        assert db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
          JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Gold'
          AND d.status_presenca='nativa' AND d.pode_ser_registrada='sim' AND d.fonte_url LIKE '%encounters.csv'""").fetchone()[0] == 1
        assert db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d JOIN JOGO j USING(id_jogo)
          WHERE j.nome IN ('Red','Blue') AND d.fonte_url LIKE '%encounters.csv'""").fetchone()[0] == 0
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


def test_context_import_preserves_curated_rows(app):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        row=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Gold'""").fetchone()
        db.execute("UPDATE DADOS_FORMA_JOGO SET motivo_registro='FIXTURE curated note' WHERE id_dados_forma=?",(row[0],))
        db.commit()
        importar_catalogo()
        assert db.execute('SELECT motivo_registro FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(row[0],)).fetchone()[0]=='FIXTURE curated note'


def test_catalog_image_mapping_uses_unambiguous_source_identifier(app, client):
    with app.app_context():
        importar_catalogo()
    result=client.get('/api/pokemon?busca=bulbasaur').json
    item=next(row for row in result['itens'] if row['codigo_forma']=='bulbasaur')
    assert item['imagem_url'].endswith('/sprites/pokemon/1.png')
    assert 'c0542f7c51215d9672439012838c99f520596cbd' in item['imagem_url']
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO ESPECIE(numero_nacional,nome_pt) VALUES(99902,'FIXTURE other species')")
        species=db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.execute("INSERT INTO FORMA(id_especie,codigo_forma,nome_forma) VALUES(?,'bulbasaur','FIXTURE different form')",(species,))
        db.commit()
    results=client.get('/api/pokemon?busca=bulbasaur').json['itens']
    unrelated=next(row for row in results if row['numero_nacional']==99902)
    assert unrelated['imagem_url'] is None


def test_real_catalog_to_owned_specimen_and_repeat_import(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        first = importar_catalogo()
        db = get_db()
        gold = db.execute("SELECT id_jogo FROM JOGO WHERE nome='Gold'").fetchone()[0]
    result = client.get('/api/pokemon', query_string={'busca':'pikachu','jogo':gold})
    assert result.status_code == 200
    row = next(x for x in result.json['itens'] if x['codigo_forma']=='pikachu')
    assert len(row['fichas']) == 1
    sheet = row['fichas'][0]
    assert sheet['status_presenca'] == 'nativa'
    assert sheet['fonte_url'].endswith('/encounters.csv')
    added = client.post('/api/colecao', json={'id_dados_forma_atual':sheet['id_dados_forma'], 'apelido':'TESTE real'}, headers={'X-CSRF-Token':get_csrf(client)})
    assert added.status_code == 201
    identifier=added.json['id_pokemon_colecao']
    with app.app_context():
        assert importar_catalogo()['fichas_encontro_documentado']==first['fichas_encontro_documentado']
    assert client.get(f'/api/colecao/{identifier}').json['apelido']=='TESTE real'


def test_sword_real_context_mechanics_and_explainable_comparison(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        importar_catalogo()
        db=get_db()
        context=db.execute("""SELECT d.id_dados_forma,m.id_mecanica FROM DADOS_FORMA_JOGO d
            JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
            WHERE f.codigo_forma='pikachu' AND j.nome='Sword' AND m.versao='regras-gerais-documentadas'""").fetchone()
        nature=db.execute("SELECT id_natureza FROM NATUREZA WHERE nome='Timid'").fetchone()[0]
        systems={row['codigo']:row['id_mecanica_sistema_atributo'] for row in db.execute("""SELECT s.codigo,m.id_mecanica_sistema_atributo FROM MECANICA_SISTEMA_ATRIBUTO m
            JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) WHERE m.id_mecanica=?""", (context['id_mecanica'],))}
        attrs={row['codigo']:row['id_atributo'] for row in db.execute('SELECT codigo,id_atributo FROM ATRIBUTO_BATALHA')}
    def val(system, attribute, value, field='valor'):
        return {'id_mecanica_sistema_atributo':systems[system],'id_atributo':attrs[attribute],field:value}
    headers={'X-CSRF-Token':get_csrf(client)}
    specimen=client.post('/api/colecao',headers=headers,json={'id_dados_forma_atual':context['id_dados_forma'],
        'id_mecanica':context['id_mecanica'],'id_natureza':nature,'nivel':50,
        'valores':[val('IV','attack',0),val('EV','speed',252)]})
    assert specimen.status_code==201, specimen.json
    profile=client.post('/api/perfis',headers=headers,json={'id_dados_forma':context['id_dados_forma'],
        'id_mecanica':context['id_mecanica'],'nome_perfil':'TESTE alvo baixo', 'naturezas':[nature],
        'valores':[val('IV','attack',0,'valor_alvo'),val('EV','speed',4,'valor_alvo')]})
    assert profile.status_code==201, profile.json
    result=client.post('/api/analises',headers=headers,json={'id_pokemon_colecao':specimen.json['id_pokemon_colecao'],'id_perfil':profile.json['id_perfil']})
    assert result.status_code==200
    attack=next(r for r in result.json['campos'] if r['sistema']=='IV' and r['atributo']=='attack')
    speed=next(r for r in result.json['campos'] if r['sistema']=='EV' and r['atributo']=='speed')
    assert attack['real']==0 and attack['estado']=='igual'
    assert speed['diferenca']==248 and speed['estado']=='acima'
    assert 'não significa melhor' in result.json['interpretacao']
    for invalid in [[val('IV','attack',32)], [val('EV','attack',253)],
                    [val('EV','attack',252),val('EV','defense',252),val('EV','speed',7)]]:
        failed=client.post('/api/colecao',headers=headers,json={'id_dados_forma_atual':context['id_dados_forma'],
            'id_mecanica':context['id_mecanica'],'valores':invalid})
        assert failed.status_code==400
    assert client.get('/api/colecao').json['total']==1


def test_curated_mechanics_conflict_aborts_without_overwrite(app):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        row=db.execute("""SELECT ms.id_mecanica_sistema_atributo FROM MECANICA_SISTEMA_ATRIBUTO ms
            JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) JOIN MECANICA_JOGO m USING(id_mecanica)
            JOIN JOGO j USING(id_jogo) WHERE j.nome='Sword' AND s.codigo='IV'""").fetchone()
        db.execute('UPDATE MECANICA_SISTEMA_ATRIBUTO SET valor_maximo_atributo=30 WHERE id_mecanica_sistema_atributo=?',(row[0],))
        db.commit()
        with pytest.raises(ValueError, match='Conflito de curadoria'):
            importar_catalogo()
        assert db.execute('SELECT valor_maximo_atributo FROM MECANICA_SISTEMA_ATRIBUTO WHERE id_mecanica_sistema_atributo=?',(row[0],)).fetchone()[0]==30


def test_history_uses_closest_applicable_change_and_preserves_empty_slot():
    from pokeanalyzer.contextual_data import _historical_rows
    current={'1':{'ability_id':'9'}, '2':{'ability_id':'8'}, '3':{'ability_id':'7'}}
    past={'1':[{'generation_id':'7','ability_id':'4'}, {'generation_id':'9','ability_id':'5'},
               {'generation_id':'8','ability_id':'6'}],
          '2':[{'generation_id':'6','ability_id':'3'}],
          '3':[{'generation_id':'8','ability_id':''}]}
    assert _historical_rows(current,past,8,'ability_id') == {'1':'6','2':'8','3':''}


def test_sword_context_has_independent_sources_and_real_values(app, client):
    with app.app_context():
        coverage=importar_catalogo()
        db=get_db()
        sword=db.execute("SELECT id_jogo FROM JOGO WHERE nome='Sword'").fetchone()[0]
        electric=db.execute("SELECT id_tipo FROM TIPO WHERE nome_tipo='Electric'").fetchone()[0]
    result=client.get('/api/pokemon',query_string={'busca':'pikachu','jogo':sword,'tipo':electric})
    row=next(x for x in result.json['itens'] if x['codigo_forma']=='pikachu')
    sheet=row['fichas'][0]
    assert sheet['tipos']==['Electric']
    assert sheet['fonte_url'].endswith('/encounters.csv')
    assert sheet['fonte_tipos'] and sheet['data_verificacao_tipos']
    detail=client.get('/api/pokemon/'+str(sheet['id_dados_forma'])).json
    assert [detail[k] for k in ('hp_base','ataque_base','defesa_base','ataque_especial_base','defesa_especial_base','velocidade_base')]==[35,55,40,50,50,90]
    assert detail['fonte_estatisticas'] and detail['data_verificacao_estatisticas']
    assert {'Static','Lightning Rod'} <= {x['nome'] for x in detail['habilidades']}
    assert all(x['fonte_url'] and x['data_verificacao'] for x in detail['habilidades'])
    assert coverage['fichas_tipos_com_fonte']>0


def test_sword_context_reimport_preserves_existing_curated_values(app):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Sword'""").fetchone()[0]
        db.execute('UPDATE DADOS_FORMA_JOGO SET hp_base=42 WHERE id_dados_forma=?',(sheet,))
        ability=db.execute('SELECT id_habilidade_forma FROM HABILIDADE_FORMA_JOGO WHERE id_dados_forma=? LIMIT 1',(sheet,)).fetchone()[0]
        db.execute("UPDATE HABILIDADE_FORMA_JOGO SET slot='FIXTURE curated' WHERE id_habilidade_forma=?",(ability,))
        db.commit()
        importar_catalogo()
        assert db.execute('SELECT hp_base FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(sheet,)).fetchone()[0]==42
        assert db.execute('SELECT slot FROM HABILIDADE_FORMA_JOGO WHERE id_habilidade_forma=?',(ability,)).fetchone()[0]=='FIXTURE curated'


def test_official_series_14_eligibility_is_conditional_and_contextual(app, client):
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Sword'""").fetchone()[0]
        rule=db.execute("""SELECT r.id_regulamento FROM REGULAMENTO r JOIN MECANICA_JOGO m USING(id_mecanica)
            JOIN JOGO j USING(id_jogo) WHERE j.nome='Sword' AND r.codigo='ranked-battles-series-14'""").fetchone()[0]
        shield_rule=db.execute("""SELECT r.id_regulamento FROM REGULAMENTO r JOIN MECANICA_JOGO m USING(id_mecanica)
            JOIN JOGO j USING(id_jogo) WHERE j.nome='Shield' AND r.codigo='ranked-battles-series-14'""").fetchone()[0]
        assert report['contagens_banco']['REGULAMENTO']==2
    result=client.get(f'/api/regulamentos/{rule}/formas/{sheet}')
    assert result.status_code==200
    assert result.json['status']=='condicional' and 'battle-ready' in result.json['condicao']
    assert 'pokemon.com' in result.json['fonte_url'] and result.json['legalidade_completa_verificada'] is False
    assert client.get(f'/api/regulamentos/{shield_rule}/formas/{sheet}').status_code==400
    with app.app_context():
        assert importar_catalogo()['contagens_banco']['REGULAMENTO']==2
        db=get_db()
        db.execute("UPDATE ELEGIBILIDADE_FORMA_REGULAMENTO SET status='proibido' WHERE id_regulamento=? AND id_dados_forma=?",(rule,sheet))
        db.commit()
        with pytest.raises(ValueError,match='Conflito de curadoria'):
            importar_catalogo()
        assert db.execute('SELECT status FROM ELEGIBILIDADE_FORMA_REGULAMENTO WHERE id_regulamento=? AND id_dados_forma=?',(rule,sheet)).fetchone()[0]=='proibido'


def test_reference_dragapult_targets_are_sourced_and_no_other_values_inferred(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        row=db.execute("""SELECT d.id_dados_forma,m.id_mecanica,p.id_perfil FROM DADOS_FORMA_JOGO d
            JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
            JOIN PERFIL_ANALISE p ON p.id_dados_forma=d.id_dados_forma AND p.id_mecanica=m.id_mecanica
            WHERE f.codigo_forma='dragapult' AND j.nome='Sword' AND p.tipo_perfil='referencia_competitiva'""").fetchone()
        values=db.execute("""SELECT a.codigo,v.valor_alvo FROM VALOR_PERFIL_ANALISE v JOIN ATRIBUTO_BATALHA a USING(id_atributo)
            WHERE id_perfil=?""",(row['id_perfil'],)).fetchall()
        assert dict(values)=={'hp':4,'attack':252,'speed':252}
        assert report['perfis_referencia_guia_vgc']==2
        assert importar_catalogo()['perfis_referencia_guia_vgc']==2
    profiles=client.get('/api/perfis').json['itens']
    ref=next(p for p in profiles if p['id_perfil']==row['id_perfil'])
    assert ref['fonte_url']=='https://www.vgcguide.com/ev-training'
    assert not ref['naturezas'] and not ref['habilidades']
    specimen=client.post('/api/colecao',headers={'X-CSRF-Token':get_csrf(client)},json={
        'id_dados_forma_atual':row['id_dados_forma'],'id_mecanica':row['id_mecanica']})
    assert specimen.status_code==201
    result=client.post('/api/analises',headers={'X-CSRF-Token':get_csrf(client)},json={
        'id_pokemon_colecao':specimen.json['id_pokemon_colecao'],'id_perfil':row['id_perfil']})
    assert result.status_code==200
    hp=next(x for x in result.json['campos'] if x['sistema']=='EV' and x['atributo']=='hp')
    assert hp['alvo']==4 and hp['real'] is None and hp['estado']=='sem_dado'
