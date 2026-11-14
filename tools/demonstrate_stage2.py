"""Professor's reproducible scenario: NEW temporary DB, explicitly synthetic facts, real HTTP handlers."""
from pathlib import Path
import json
import tempfile
from pokeanalyzer import create_app
from pokeanalyzer.db import init_db, get_db


def demonstrate():
    with tempfile.TemporaryDirectory(prefix='pokelizer-FIXTURE-') as folder:
        app=create_app({'TESTING':True,'SECRET_KEY':'fixture-only','DATABASE':str(Path(folder)/'fixture.sqlite3')})
        init_db(app)
        with app.app_context():
            db=get_db()
            db.executescript((Path(__file__).resolve().parents[1]/'backend/tests/fixtures/catalog.sql').read_text())
            db.executescript("""
            INSERT INTO ATRIBUTO_BATALHA VALUES(1,'fixture-attack','FIXTURE Attack');
            INSERT INTO SISTEMA_ATRIBUTO VALUES(1,'fixture-system','FIXTURE system',NULL);
            INSERT INTO MECANICA_SISTEMA_ATRIBUTO(id_mecanica_sistema_atributo,id_mecanica,id_sistema_atributo,aplicabilidade,valor_minimo,valor_maximo_atributo,limite_total_status,fonte_url,data_verificacao)
            VALUES(1,1,1,'aplicavel',0,10,'nao_aplicavel','https://example.invalid/fixture','2026-11-13');
            INSERT INTO MECANICA_ATRIBUTO VALUES(1,1,'aplicavel','https://example.invalid/fixture','2026-11-13');
            """)
        client=app.test_client()
        def request(method,url,body=None,expected=200):
            token=client.get('/api/csrf').json['csrf_token']
            response=client.open(url,method=method,json=body,headers={'X-CSRF-Token':token})
            assert response.status_code==expected,(url,response.status_code,response.json)
            print(f'{method} {url}: {response.status_code}')
            return response.json
        request('POST','/api/auth/cadastro',{'nome_usuario':'FIXTURE professor','email':'fixture@example.invalid','senha':'fixture-password'},201)
        value={'id_mecanica_sistema_atributo':1,'id_atributo':1,'valor':0}
        specimen=request('POST','/api/colecao',{'id_dados_forma_atual':1,'id_mecanica':1,'valores':[value]},201)
        path=f"/api/colecao/{specimen['id_pokemon_colecao']}"
        request('GET',path)
        request('PATCH',path,{'apelido':'FIXTURE edited'})
        profile=request('POST','/api/perfis',{'id_dados_forma':1,'id_mecanica':1,'nome_perfil':'FIXTURE target','valores':[{'id_mecanica_sistema_atributo':1,'id_atributo':1,'valor_alvo':2}]},201)
        analysis=request('POST','/api/analises',{'id_pokemon_colecao':specimen['id_pokemon_colecao'],'id_perfil':profile['id_perfil']})
        assert analysis['campos'][0]['real']==0 and analysis['campos'][0]['estado']=='abaixo'
        print(json.dumps(analysis['campos'],ensure_ascii=False,indent=2))
        request('POST','/api/colecao',{'id_dados_forma_atual':1,'campo_ignorado':True},400)
        request('GET','/api/pokemon?busca=fixture-standard')
        request('DELETE',path,{})
        request('DELETE',f"/api/perfis/{profile['id_perfil']}",{})
        assert client.get('/api/colecao').json['total']==0
        with app.app_context():
            assert not get_db().execute('PRAGMA foreign_key_check').fetchall()
        print('Demonstração concluída. Banco FIXTURE temporário removido; nenhum dado pessoal ou fato Pokémon inventado.')


if __name__=='__main__':
    demonstrate()
