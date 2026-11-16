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
        assert c['versoes_identificadas']==c['versoes_fonte']==53
        assert db.execute('SELECT nome_usuario FROM USUARIO').fetchone()[0]=='FIXTURE preserved'
        assert db.execute("SELECT count(*) FROM ESPECIE WHERE nome_en='Pikachu'").fetchone()[0]==1
        assert first['fichas_encontro_documentado'] >= 5000
        assert first['fichas_outras_fontes_preservadas'] == 1
        assert db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
          JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Gold'
          AND d.status_presenca='nativa' AND d.pode_ser_registrada='sim' AND d.fonte_url LIKE '%encounters.csv'""").fetchone()[0] == 1
        versions=db.execute("""SELECT j.codigo_versao_pokeapi,count(d.id_dados_forma) FROM JOGO j
          LEFT JOIN DADOS_FORMA_JOGO d USING(id_jogo) WHERE j.codigo_versao_pokeapi IN ('red','red-japan','blue','blue-japan')
          GROUP BY j.id_jogo""").fetchall()
        by_version=dict(versions)
        assert set(by_version)=={'red','red-japan','blue','blue-japan'}
        assert all(by_version[v]>0 for v in ('red','red-japan','blue'))
        # Blue japonesa possui presentes documentados; não há encontros selvagens
        # cujo grupo de versão coincida com o da ficha neste snapshot.
        assert by_version['blue-japan'] > 0
        assert db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d
          JOIN JOGO j USING(id_jogo) JOIN METODO_FORMA_JOGO mf USING(id_dados_forma)
          JOIN METODO_OBTENCAO m USING(id_metodo)
          WHERE j.codigo_versao_pokeapi='blue-japan' AND m.nome='Encontro selvagem'""").fetchone()[0] == 0
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


def test_real_historical_contexts_preserve_generation_differences(app, client):
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        def sheet(form, game):
            return db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
                JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma=? AND j.nome=?""",(form,game)).fetchone()[0]
        clefairy_gold,clefairy_x=sheet('clefairy','Gold'),sheet('clefairy','X')
        magnemite_yellow,magnemite_gold=sheet('magnemite','Yellow'),sheet('magnemite','Gold')
        chansey_yellow,hypno_red=sheet('chansey','Yellow'),sheet('hypno','Red (red)')
        pikachu_gold,gengar_diamond=sheet('pikachu','Gold'),sheet('gengar','Diamond')
        pikachu_diamond,pikachu_x=sheet('pikachu','Diamond'),sheet('pikachu','X')
        poochyena_ruby=sheet('poochyena','Ruby')
        assert report['fichas_tipos_com_fonte'] >= 5000
        assert report['fichas_estatisticas_com_fonte'] >= 4800
        coverage={g['nome']:g for g in report['cobertura_por_jogo']}
        assert coverage['Yellow']['tipos_com_fonte']==coverage['Yellow']['fichas']>0
        assert coverage['Yellow']['seis_estatisticas_com_fonte']==0
        assert coverage['Yellow']['cinco_estatisticas_especial_unico_com_fonte']==coverage['Yellow']['fichas']
        assert coverage['Gold']['fichas_com_alguma_habilidade_com_fonte']==0
        assert coverage['Diamond']['fichas_com_alguma_habilidade_com_fonte']>0
    def details(identifier):
        response=client.get(f'/api/pokemon/{identifier}')
        assert response.status_code==200
        return response.json
    assert details(clefairy_gold)['tipos']==['Normal']
    assert details(clefairy_x)['tipos']==['Fairy']
    yellow=details(magnemite_yellow)
    assert yellow['tipos']==['Electric']
    assert yellow['hp_base']==25 and yellow['especial_base']==95
    assert yellow['ataque_especial_base'] is None and yellow['defesa_especial_base'] is None
    assert yellow['fonte_estatisticas'] and yellow['data_verificacao_estatisticas']
    assert details(chansey_yellow)['especial_base']==105  # Modern Special Attack is 35, not this value.
    assert details(hypno_red)['especial_base']==115  # Modern Special Attack is 73.
    assert yellow['estado_sistema_estatisticas']=='especial_unico' and yellow['fonte_sistema_estatisticas']
    assert yellow['estado_sistema_habilidades']=='nao_aplicavel'
    assert yellow['fonte_sistema_habilidades'] and not yellow['habilidades']
    assert details(magnemite_gold)['tipos']==['Electric','Steel']
    pika=details(pikachu_gold)
    assert [pika[k] for k in ('hp_base','ataque_base','defesa_base','ataque_especial_base','defesa_especial_base','velocidade_base')]==[35,55,30,50,40,90]
    assert pika['estado_sistema_habilidades']=='nao_aplicavel' and not pika['habilidades']
    gengar=details(gengar_diamond)
    assert [h['nome'] for h in gengar['habilidades']]==['Levitate']
    assert gengar['habilidades'][0]['condicao'] and gengar['habilidades'][0]['fonte_url']
    assert [h['nome'] for h in details(poochyena_ruby)['habilidades']]==['Run Away']
    assert [h['nome'] for h in details(pikachu_diamond)['habilidades']]==['Static']
    assert {h['nome'] for h in details(pikachu_x)['habilidades']}=={'Static','Lightning Rod'}


def test_distinct_red_blue_versions_report_first_generation_rules(app, client):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        rows=db.execute("""SELECT j.codigo_versao_pokeapi,j.id_jogo,d.id_dados_forma FROM JOGO j
            JOIN DADOS_FORMA_JOGO d USING(id_jogo) JOIN FORMA f USING(id_forma)
            WHERE j.codigo_versao_pokeapi IN ('red','red-japan','blue','blue-japan')
            AND f.codigo_forma='pikachu' ORDER BY j.codigo_versao_pokeapi""").fetchall()
        # The snapshot supplies a wild Pikachu encounter only for versions with these rows;
        # absence of a row does not imply absence in a version.
        assert len(rows)>=2 and len({r['id_jogo'] for r in rows})==len(rows)
    for row in rows:
        detail=client.get(f"/api/pokemon/{row['id_dados_forma']}").json
        assert detail['codigo_versao_pokeapi']==row['codigo_versao_pokeapi']
        assert detail['estado_sistema_estatisticas']=='especial_unico'
        assert detail['estado_sistema_habilidades']=='nao_aplicavel'
        assert detail['tipos']==['Electric']


def test_historical_real_mechanics_have_distinct_ev_limits_and_contexts(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        assert report['contagens_banco']['MECANICA_JOGO']==36  # 22 históricas, 9 antigas, 2 SwSh, 2 SV, 1 FIXTURE
        contexts={}
        for game in ('ruby','x'):
            row=db.execute("""SELECT d.id_dados_forma,m.id_mecanica,ms.id_mecanica_sistema_atributo,
                    ms.valor_maximo_atributo,ms.valor_maximo_total,ms.fonte_url
                FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo)
                JOIN MECANICA_JOGO m USING(id_jogo) JOIN MECANICA_SISTEMA_ATRIBUTO ms USING(id_mecanica)
                JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo)
                WHERE f.codigo_forma='pikachu' AND j.codigo_versao_pokeapi=? AND s.codigo='EV'""",(game,)).fetchone()
            contexts[game]=dict(row)
        attr=db.execute("SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo='attack'").fetchone()[0]
        assert contexts['ruby']['valor_maximo_atributo']==255
        assert contexts['x']['valor_maximo_atributo']==252
        assert all(c['valor_maximo_total']==510 and c['fonte_url'].endswith('/Effort_values') for c in contexts.values())
        assert not db.execute("""SELECT 1 FROM MECANICA_JOGO m JOIN JOGO j USING(id_jogo)
                               WHERE j.codigo_versao_pokeapi IN ('lets-go-pikachu','legends-arceus')""").fetchall()
    headers={'X-CSRF-Token':get_csrf(client)}
    def value(context,number,field='valor'):
        return {'id_mecanica_sistema_atributo':context['id_mecanica_sistema_atributo'],'id_atributo':attr,field:number}
    ruby,x=contexts['ruby'],contexts['x']
    specimen=client.post('/api/colecao',headers=headers,json={'id_dados_forma_atual':ruby['id_dados_forma'],
        'id_mecanica':ruby['id_mecanica'],'valores':[value(ruby,255)]})
    assert specimen.status_code==201, specimen.json
    for context,number in ((ruby,256),(x,253)):
        rejected=client.post('/api/colecao',headers=headers,json={'id_dados_forma_atual':context['id_dados_forma'],
            'id_mecanica':context['id_mecanica'],'valores':[value(context,number)]})
        assert rejected.status_code==400
    profile=client.post('/api/perfis',headers=headers,json={'id_dados_forma':ruby['id_dados_forma'],
        'id_mecanica':ruby['id_mecanica'],'nome_perfil':'FIXTURE alvo 252','valores':[value(ruby,252,'valor_alvo')]})
    assert profile.status_code==201, profile.json
    compared=client.post('/api/analises',headers=headers,json={'id_pokemon_colecao':specimen.json['id_pokemon_colecao'],
                                                             'id_perfil':profile.json['id_perfil']})
    attack=next(v for v in compared.json['campos'] if v['sistema']=='EV' and v['atributo']=='attack')
    assert attack['real']==255 and attack['alvo']==252 and attack['diferenca']==3 and attack['estado']=='acima'
    assert 'não significa melhor' in compared.json['interpretacao']
    wrong=client.post('/api/perfis',headers=headers,json={'id_dados_forma':ruby['id_dados_forma'],
        'id_mecanica':x['id_mecanica'],'nome_perfil':'FIXTURE contexto incompatível'})
    assert wrong.status_code==400


def test_historical_mechanics_conflict_preserves_curation(app):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        row=db.execute("""SELECT ms.id_mecanica_sistema_atributo FROM MECANICA_SISTEMA_ATRIBUTO ms
            JOIN MECANICA_JOGO m USING(id_mecanica) JOIN JOGO j USING(id_jogo)
            JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo)
            WHERE j.codigo_versao_pokeapi='ruby' AND s.codigo='EV'""").fetchone()
        db.execute('UPDATE MECANICA_SISTEMA_ATRIBUTO SET valor_maximo_atributo=254 WHERE id_mecanica_sistema_atributo=?',(row[0],))
        db.commit()
        with pytest.raises(ValueError,match='Conflito de curadoria'):
            importar_catalogo()
        assert db.execute('SELECT valor_maximo_atributo FROM MECANICA_SISTEMA_ATRIBUTO WHERE id_mecanica_sistema_atributo=?',(row[0],)).fetchone()[0]==254


def test_early_real_games_allow_level_without_inventing_modern_systems(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        importar_catalogo()
        db=get_db()
        contexts={}
        for game,form in [('yellow','magnemite'),('gold','pikachu')]:
            row=db.execute("""SELECT d.id_dados_forma,m.id_mecanica,m.usa_natureza,m.usa_habilidade,
                    m.nivel_minimo,m.nivel_maximo FROM DADOS_FORMA_JOGO d
                JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
                WHERE f.codigo_forma=? AND j.codigo_versao_pokeapi=?""",(form,game)).fetchone()
            contexts[game]=dict(row)
            assert row['usa_natureza']==row['usa_habilidade']=='nao'
            assert (row['nivel_minimo'],row['nivel_maximo'])==(1,100)
            systems=db.execute("""SELECT s.codigo,m.valor_maximo_atributo FROM MECANICA_SISTEMA_ATRIBUTO m
                JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) WHERE m.id_mecanica=?""",(row['id_mecanica'],)).fetchall()
            assert dict(systems)=={'DV':15,'STAT_EXP':65535}
        nature=db.execute("SELECT id_natureza FROM NATUREZA WHERE nome='Timid'").fetchone()[0]
    headers={'X-CSRF-Token':get_csrf(client)}
    yellow=contexts['yellow']
    body={'id_dados_forma_atual':yellow['id_dados_forma'],'id_mecanica':yellow['id_mecanica'],'nivel':50}
    specimen=client.post('/api/colecao',headers=headers,json=body)
    assert specimen.status_code==201,specimen.json
    assert client.get('/api/colecao/'+str(specimen.json['id_pokemon_colecao'])).json['nivel']==50
    assert client.post('/api/colecao',headers=headers,json=body|{'nivel':101}).status_code==400
    assert client.post('/api/colecao',headers=headers,json=body|{'id_natureza':nature}).status_code==400
    profile=client.post('/api/perfis',headers=headers,json={'id_dados_forma':yellow['id_dados_forma'],
        'id_mecanica':yellow['id_mecanica'],'nome_perfil':'FIXTURE regras antigas'})
    assert profile.status_code==201,profile.json
    result=client.post('/api/analises',headers=headers,json={'id_pokemon_colecao':specimen.json['id_pokemon_colecao'],
                                                           'id_perfil':profile.json['id_perfil']})
    assert result.status_code==200
    hp=next(row for row in result.json['campos'] if row['atributo']=='hp (derivado)')
    assert hp['real'] is None and hp['estado_real']=='ausente'
    assert all(row['estado']=='nao_aplicavel' for row in result.json['preferencias'])


def test_early_values_derive_hp_preserve_unknown_and_validate_limits(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        importar_catalogo()
        db=get_db()
        context=db.execute("""SELECT d.id_dados_forma,m.id_mecanica FROM DADOS_FORMA_JOGO d
            JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
            WHERE f.codigo_forma='magnemite' AND j.codigo_versao_pokeapi='yellow'""").fetchone()
        systems={row['codigo']:row['id_mecanica_sistema_atributo'] for row in db.execute("""SELECT s.codigo,m.id_mecanica_sistema_atributo
            FROM MECANICA_SISTEMA_ATRIBUTO m JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) WHERE id_mecanica=?""",(context['id_mecanica'],))}
        attrs={row['codigo']:row['id_atributo'] for row in db.execute('SELECT codigo,id_atributo FROM ATRIBUTO_BATALHA')}
    mechanic=client.get('/api/mecanicas/'+str(context['id_mecanica'])).json
    choices={s['codigo']:{a['codigo'] for a in s['atributos']} for s in mechanic['sistemas']}
    assert choices=={'DV':{'attack','defense','speed','special'},'STAT_EXP':{'hp','attack','defense','speed','special'}}
    assert all(s['descricao_sistema'] for s in mechanic['sistemas'])
    def value(system,attribute,number,field='valor',state='conhecido'):
        return {'id_mecanica_sistema_atributo':systems[system],'id_atributo':attrs[attribute],field:number,'estado':state}
    headers={'X-CSRF-Token':get_csrf(client)}
    actual=[value('DV',code,n) for code,n in [('attack',15),('defense',14),('speed',13),('special',12)]]
    actual += [value('STAT_EXP','hp',65535),value('STAT_EXP','attack',0)]
    body={'id_dados_forma_atual':context['id_dados_forma'],'id_mecanica':context['id_mecanica'],'valores':actual}
    specimen=client.post('/api/colecao',headers=headers,json=body)
    assert specimen.status_code==201,specimen.json
    targets=[value('DV',code,n,'valor_alvo') for code,n in [('attack',14),('defense',15),('speed',12),('special',13)]]
    profile=client.post('/api/perfis',headers=headers,json={'id_dados_forma':context['id_dados_forma'],
        'id_mecanica':context['id_mecanica'],'nome_perfil':'FIXTURE DV alvo','valores':targets})
    assert profile.status_code==201,profile.json
    payload={'id_pokemon_colecao':specimen.json['id_pokemon_colecao'],'id_perfil':profile.json['id_perfil']}
    comparison=client.post('/api/analises',headers=headers,json=payload).json
    hp=next(row for row in comparison['campos'] if row['atributo']=='hp (derivado)')
    assert (hp['real'],hp['alvo'],hp['diferenca'],hp['estado'])==(10,5,5,'acima')
    assert hp['derivado'] and hp['explicacao']
    assert next(row for row in comparison['campos'] if row['sistema']=='STAT_EXP' and row['atributo']=='attack')['real']==0
    targets[-1]=value('DV','special',None,'valor_alvo','desconhecido')
    assert client.patch('/api/perfis/'+str(profile.json['id_perfil']),headers=headers,json={'valores':targets}).status_code==200
    hp=next(row for row in client.post('/api/analises',headers=headers,json=payload).json['campos'] if row['atributo']=='hp (derivado)')
    assert hp['alvo'] is None and hp['estado_alvo']=='desconhecido' and hp['diferenca'] is None
    for invalid in (value('DV','attack',16),value('DV','hp',1),value('STAT_EXP','special',65536)):
        failed=client.post('/api/colecao',headers=headers,json=body|{'valores':[value('STAT_EXP','hp',1),invalid]})
        assert failed.status_code==400
    assert client.get('/api/colecao').json['total']==1
    with app.app_context():
        importar_catalogo()
    assert len(client.get('/api/colecao/'+str(specimen.json['id_pokemon_colecao'])).json['valores'])==len(actual)


def test_adding_early_systems_preserves_existing_specimen(app, client, monkeypatch):
    from test_api import create_user, get_csrf
    import pokeanalyzer.curated_data as curated
    def old_partial(db, data):
        game=db.execute("SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi='yellow'").fetchone()[0]
        db.execute("""INSERT INTO MECANICA_JOGO(id_jogo,versao,usa_natureza,usa_habilidade,usa_nivel,
                   nivel_minimo,nivel_maximo,fonte_url,data_verificacao)
                   VALUES(?,'regras-parciais-documentadas','nao','nao','sim',1,100,?,?)""",
                   (game,curated.ABILITY_SOURCE,curated.HISTORICAL_DATE))
    with app.app_context(), monkeypatch.context() as patch:
        patch.setattr(curated,'importar_mecanicas_anteriores',old_partial)
        importar_catalogo()
        db=get_db()
        context=db.execute("""SELECT d.id_dados_forma,m.id_mecanica FROM DADOS_FORMA_JOGO d
            JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
            WHERE f.codigo_forma='magnemite' AND j.codigo_versao_pokeapi='yellow'""").fetchone()
        sheet,mechanic=tuple(context)
    create_user(client)
    specimen=client.post('/api/colecao',headers={'X-CSRF-Token':get_csrf(client)},
        json={'id_dados_forma_atual':sheet,'id_mecanica':mechanic,'nivel':55,'apelido':'FIXTURE preservado'})
    assert specimen.status_code==201
    with app.app_context():
        importar_catalogo()
        db=get_db()
        assert db.execute('SELECT count(*) FROM MECANICA_SISTEMA_ATRIBUTO WHERE id_mecanica=?',(mechanic,)).fetchone()[0]==2
    stored=client.get('/api/colecao/'+str(specimen.json['id_pokemon_colecao'])).json
    assert (stored['id_mecanica'],stored['nivel'],stored['apelido'],stored['valores'])==(mechanic,55,'FIXTURE preservado',[])


def test_early_special_code_conflict_aborts_without_reinterpreting_existing_data(app):
    with app.app_context():
        db=get_db()
        db.execute("INSERT INTO ATRIBUTO_BATALHA(codigo,nome) VALUES('special','FIXTURE outro significado')")
        db.commit()
        species_before=db.execute('SELECT count(*) FROM ESPECIE').fetchone()[0]
        with pytest.raises(ValueError,match='Conflito de curadoria'):
            importar_catalogo()
        assert db.execute("SELECT nome FROM ATRIBUTO_BATALHA WHERE codigo='special'").fetchone()[0]=='FIXTURE outro significado'
        assert db.execute('SELECT count(*) FROM ESPECIE').fetchone()[0]==species_before


def test_generation_one_stats_preserve_partial_existing_curation(app, monkeypatch):
    import pokeanalyzer.contextual_data as contextual
    with app.app_context(), monkeypatch.context() as patch:
        patch.setattr(contextual,'importar_contextos_por_geracao',lambda *_:None)
        importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='magnemite' AND j.codigo_versao_pokeapi='yellow'""").fetchone()[0]
        db.execute('UPDATE DADOS_FORMA_JOGO SET hp_base=42 WHERE id_dados_forma=?',(sheet,))
        db.commit()
    with app.app_context():
        importar_catalogo()
        row=get_db().execute('SELECT hp_base,ataque_base,especial_base,fonte_estatisticas FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(sheet,)).fetchone()
        assert tuple(row)==(42,None,None,None)


def test_historical_stats_do_not_mix_with_existing_special_curated_value(app, monkeypatch):
    import pokeanalyzer.contextual_data as contextual
    with app.app_context(), monkeypatch.context() as patch:
        patch.setattr(contextual,'importar_contextos_por_geracao',lambda *_:None)
        importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.codigo_versao_pokeapi='gold'""").fetchone()[0]
        db.execute('UPDATE DADOS_FORMA_JOGO SET especial_base=42 WHERE id_dados_forma=?',(sheet,))
        db.commit()
    with app.app_context():
        report=importar_catalogo()
        row=get_db().execute('SELECT hp_base,ataque_especial_base,especial_base,fonte_estatisticas FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(sheet,)).fetchone()
        assert tuple(row)==(None,None,42,None)
        assert report['fichas_com_sistemas_estatisticos_misturados']==0
        get_db().execute('UPDATE DADOS_FORMA_JOGO SET ataque_especial_base=99 WHERE id_dados_forma=?',(sheet,))
        from pokeanalyzer.catalog_data import cobertura
        assert cobertura()['fichas_com_sistemas_estatisticos_misturados']==1


def test_real_extended_encounters_distinguish_gifts_eggs_and_wild(app, client):
    from test_api import create_user, get_csrf
    create_user(client)
    with app.app_context():
        report=importar_catalogo()
        db=get_db()
        def sheet(form,version):
            row=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
                JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma=? AND j.codigo_versao_pokeapi=?""",(form,version)).fetchone()
            assert row,(form,version)
            return row[0]
        nickit=sheet('nickit','sword')
        pidgey=sheet('pidgey','lets-go-pikachu')
        gifted=sheet('pikachu','yellow')
        egg=sheet('togepi','gold')
        charmander=sheet('charmander','sword')
        assert report['fichas_metodo_selvagem']>6000
        assert report['fichas_metodo_presente']>200
        assert report['fichas_metodo_ovo']>0
    def details(identifier):
        response=client.get('/api/pokemon/'+str(identifier))
        assert response.status_code==200
        return response.json
    sword=details(nickit)
    assert sword['status_presenca']=='nativa' and sword['pode_ser_registrada']=='sim'
    assert sword['tipos']==['Dark'] and any('Walking in the overworld' in (m['condicao'] or '') for m in sword['metodos'])
    assert all(m['fonte_url'].endswith('/encounters.csv') for m in sword['metodos'])
    letsgo=details(pidgey)
    assert letsgo['estado_sistema_habilidades']=='nao_aplicavel' and not letsgo['habilidades']
    assert any(m['nome']=='Encontro selvagem' for m in letsgo['metodos'])
    assert [m['nome'] for m in details(gifted)['metodos']]==['Presente no jogo']
    assert [m['nome'] for m in details(egg)['metodos']]==['Ovo recebido no jogo']
    assert [m['nome'] for m in details(charmander)['metodos']]==['Presente no jogo']  # Source raid rows are not called wild or imported.
    added=client.post('/api/colecao',headers={'X-CSRF-Token':get_csrf(client)},
        json={'id_dados_forma_atual':gifted,'id_metodo_obtencao':details(gifted)['metodos'][0]['id_metodo'],'apelido':'FIXTURE presente'})
    assert added.status_code==201,added.json


def test_extended_import_preserves_owned_specimen_and_existing_method_curation(app, client, monkeypatch):
    from test_api import create_user, get_csrf
    import pokeanalyzer.catalog_data as catalog
    _,source=catalog.ler_snapshot()
    original_ids={str(n) for n in (*range(1,18),22,23,24)}
    old_names=frozenset(row['identifier'] for row in source['encounter_methods.csv'] if row['id'] in original_ids)
    with app.app_context(), monkeypatch.context() as patch:
        patch.setattr(catalog,'METHOD_GROUPS',{'Encontro selvagem':old_names})
        catalog.importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.codigo_versao_pokeapi='gold'""").fetchone()[0]
        db.execute("UPDATE METODO_FORMA_JOGO SET condicao='FIXTURE curadoria' WHERE id_dados_forma=?",(sheet,))
        db.commit()
    create_user(client)
    added=client.post('/api/colecao',headers={'X-CSRF-Token':get_csrf(client)},
        json={'id_dados_forma_atual':sheet,'apelido':'FIXTURE preservado'})
    assert added.status_code==201
    with app.app_context():
        first=catalog.importar_catalogo()
        assert catalog.importar_catalogo()==first
        db=get_db()
        assert db.execute('SELECT condicao FROM METODO_FORMA_JOGO WHERE id_dados_forma=?',(sheet,)).fetchone()[0]=='FIXTURE curadoria'
        assert db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.codigo_versao_pokeapi='yellow'""").fetchone()[0]==1
        assert not db.execute('PRAGMA foreign_key_check').fetchall()
    assert client.get('/api/colecao/'+str(added.json['id_pokemon_colecao'])).json['apelido']=='FIXTURE preservado'


def test_history_reimport_preserves_existing_specimen_and_partial_curation(app, client, monkeypatch):
    from test_api import create_user, get_csrf
    import pokeanalyzer.contextual_data as contextual
    # Represent an existing versioned database created before historical enrichment.
    with app.app_context(), monkeypatch.context() as patch:
        patch.setattr(contextual, 'importar_contextos_por_geracao', lambda *_: None)
        importar_catalogo()
        db=get_db()
        sheet=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='pikachu' AND j.nome='Gold'""").fetchone()[0]
        db.execute('UPDATE DADOS_FORMA_JOGO SET hp_base=42 WHERE id_dados_forma=?',(sheet,))
        db.commit()
    create_user(client)
    added=client.post('/api/colecao',json={'id_dados_forma_atual':sheet,'apelido':'FIXTURE preservado'},
                      headers={'X-CSRF-Token':get_csrf(client)})
    assert added.status_code==201
    with app.app_context():
        importar_catalogo()
        db=get_db()
        row=db.execute('SELECT hp_base,ataque_base,fonte_estatisticas FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(sheet,)).fetchone()
        assert tuple(row)==(42,None,None)  # Existing partial curation is not replaced or completed silently.
    assert client.get('/api/colecao/'+str(added.json['id_pokemon_colecao'])).json['apelido']=='FIXTURE preservado'
    assert client.get('/api/pokemon/'+str(sheet)).json['tipos']==['Electric']


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


def test_official_scarlet_violet_starters_have_real_contexts_and_mechanics(app, client):
    from test_api import create_user, get_csrf
    from pokeanalyzer.curated_data import SV_STARTER_SOURCE
    create_user(client)
    with app.app_context():
        report=importar_catalogo()
        assert report['fichas_iniciais_scarlet_violet']==6
        db=get_db()
        def sheet(form, version):
            return db.execute("""SELECT d.id_dados_forma,m.id_mecanica FROM DADOS_FORMA_JOGO d
                JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo) JOIN MECANICA_JOGO m USING(id_jogo)
                WHERE f.codigo_forma=? AND j.codigo_versao_pokeapi=? AND d.fonte_url=?""",
                (form,version,SV_STARTER_SOURCE)).fetchone()
        scarlet=sheet('sprigatito','scarlet');violet=sheet('sprigatito','violet')
        assert scarlet and violet
        assert all(sheet(form,version) for form in ('sprigatito','fuecoco','quaxly') for version in ('scarlet','violet'))
        ev=db.execute("""SELECT ms.id_mecanica_sistema_atributo FROM MECANICA_SISTEMA_ATRIBUTO ms
            JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo) WHERE ms.id_mecanica=? AND s.codigo='EV'""",(scarlet['id_mecanica'],)).fetchone()[0]
        speed=db.execute("SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo='speed'").fetchone()[0]
    details=client.get('/api/pokemon/'+str(scarlet['id_dados_forma'])).json
    assert details['tipos']==['Grass'] and details['hp_base']==40 and details['velocidade_base']==65
    assert details['fonte_url']==SV_STARTER_SOURCE and details['fonte_tipos'] and details['fonte_estatisticas']
    assert any(m['nome']=='Presente no jogo' and m['fonte_url']==SV_STARTER_SOURCE for m in details['metodos'])
    headers={'X-CSRF-Token':get_csrf(client)}
    value={'id_mecanica_sistema_atributo':ev,'id_atributo':speed,'valor':252}
    body={'id_dados_forma_atual':scarlet['id_dados_forma'],'id_mecanica':scarlet['id_mecanica'],
          'nivel':50,'valores':[value]}
    created=client.post('/api/colecao',headers=headers,json=body)
    assert created.status_code==201, created.json
    bad=client.post('/api/colecao',headers=headers,json={**body,'valores':[{**value,'valor':253}]})
    assert bad.status_code==400
    target={**value,'valor_alvo':4};target.pop('valor')
    profile=client.post('/api/perfis',headers=headers,json={'id_dados_forma':scarlet['id_dados_forma'],
        'id_mecanica':scarlet['id_mecanica'],'nome_perfil':'FIXTURE SV','valores':[target]})
    assert profile.status_code==201, profile.json
    analysis=client.post('/api/analises',headers=headers,json={'id_pokemon_colecao':created.json['id_pokemon_colecao'],
        'id_perfil':profile.json['id_perfil']})
    assert analysis.status_code==200 and any(x['diferenca']==248 for x in analysis.json['campos'])
    different=client.post('/api/perfis',headers=headers,json={'id_dados_forma':violet['id_dados_forma'],
        'id_mecanica':violet['id_mecanica'],'nome_perfil':'FIXTURE outra versão'})
    assert different.status_code==201
    assert client.post('/api/analises',headers=headers,json={'id_pokemon_colecao':created.json['id_pokemon_colecao'],
        'id_perfil':different.json['id_perfil']}).status_code==400
    with app.app_context():
        assert importar_catalogo()==report
        assert not get_db().execute('PRAGMA foreign_key_check').fetchall()
    assert client.get('/api/colecao/'+str(created.json['id_pokemon_colecao'])).status_code==200


def test_scarlet_starter_reimport_preserves_prior_context(app):
    with app.app_context():
        importar_catalogo()
        db=get_db()
        row=db.execute("""SELECT d.id_dados_forma FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma)
            JOIN JOGO j USING(id_jogo) WHERE f.codigo_forma='sprigatito' AND j.codigo_versao_pokeapi='scarlet'""").fetchone()
        db.execute("UPDATE DADOS_FORMA_JOGO SET fonte_url='https://example.invalid/fixture-curada',hp_base=42 WHERE id_dados_forma=?",(row[0],))
        db.commit()
        report=importar_catalogo()
        saved=db.execute('SELECT fonte_url,hp_base FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(row[0],)).fetchone()
        assert tuple(saved)==('https://example.invalid/fixture-curada',42)
        assert report['fichas_iniciais_scarlet_violet']==5
        assert report['fichas_outras_fontes_preservadas']>=1
