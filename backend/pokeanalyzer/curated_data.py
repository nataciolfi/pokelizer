"""Mechanics only for explicitly named games and documented generation limits."""

import csv
import hashlib
from pathlib import Path

OFFICIAL = 'https://www.pokemon.com/us/strategy/train-raid-and-hatch-pokemon-to-breed-victories-in-pokemon-sword-and-pokemon-shield'
IV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Individual_values'
EV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Effort_values'
NATURE_SOURCE = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/8a92bfa7dab2f12b84b5d151562f9857c133ff30/data/v2/csv/natures.csv'
DATE = '2026-11-14'
SERIES_14_SOURCE = 'https://www.pokemon.com/us/pokemon-news/pokemon-sword-and-pokemon-shield-ranked-battles-november-2022-season-season-36/'
DRAGAPULT_SOURCE = 'https://www.vgcguide.com/ev-training'
ABILITY_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Ability'
SV_STARTER_SOURCE = 'https://press.pokemon.com/en-CA/POKEMON-ANNOUNCES-NEW-VIDEO-GAMES-POKEMON-SCARLET-AND-POKEMON-VIOLET-'
SV_RAID_SOURCE = 'https://sv-news.pokemon.co.jp/en/page/261.html'
LGPE_PARTNER_SOURCE = ('https://bulbapedia.bulbagarden.net/w/index.php?title=List_of_in-game_event_Pok%C3%A9mon_in_Pok%C3%A9mon:'
                       '_Let%27s_Go,_Pikachu!_and_Let%27s_Go,_Eevee!&oldid=4559684')
LGPE_RULE_SOURCE = 'https://www.serebii.net/letsgopikachueevee/stats.shtml'
LGPE_AVAILABILITY_SOURCE = ('https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_availability_'
                            '%28Let%27s_Go%2C_Pikachu%21_and_Let%27s_Go%2C_Eevee%21%29')
LGPE_AVAILABILITY_DATE = '2026-11-17'
LGPE_AVAILABILITY_FILE = Path(__file__).resolve().parents[1] / 'data' / 'curated' / 'lgpe-availability.csv'
LGPE_AVAILABILITY_SHA256 = '19c7d64158941b727d108355699882a907d920ebfb42e63da3afa0b4e56ed7be'
LGPE_ALOLAN_FILE = Path(__file__).resolve().parents[1] / 'data' / 'curated' / 'lgpe-alolan-forms.csv'
LGPE_ALOLAN_SHA256 = '07fdd18bb51ce0250ca1b1ddd1f4b573c1c49f828213bb8230578a6d2af10190'
LGPE_ALOLAN_FORMS = {
    19:'rattata-alola',20:'raticate-alola',26:'raichu-alola',27:'sandshrew-alola',
    28:'sandslash-alola',37:'vulpix-alola',38:'ninetales-alola',50:'diglett-alola',
    51:'dugtrio-alola',52:'meowth-alola',53:'persian-alola',74:'geodude-alola',
    75:'graveler-alola',76:'golem-alola',88:'grimer-alola',89:'muk-alola',
    103:'exeggutor-alola',105:'marowak-alola',
}
LGPE_MEGA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'curated' / 'lgpe-mega-forms.csv'
LGPE_MEGA_SHA256 = '6c852fc04921f0f1433604ef0088bf9015cdb6a11b369d58b556843546533cf0'
LGPE_MEGA_FORMS = {
    3:('venusaur-mega',),6:('charizard-mega-x','charizard-mega-y'),9:('blastoise-mega',),
    15:('beedrill-mega',),18:('pidgeot-mega',),65:('alakazam-mega',),80:('slowbro-mega',),
    94:('gengar-mega',),115:('kangaskhan-mega',),127:('pinsir-mega',),130:('gyarados-mega',),
    142:('aerodactyl-mega',),150:('mewtwo-mega-x','mewtwo-mega-y'),
}
LGPE_MEGA_SOURCE = ('https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon%3A_Let%27s_Go%2C_Eevee%21')
SV_DATE = '2026-11-16'
HISTORICAL_DATE = '2026-11-15'
# Curated historical core-series versions only. Other games are added explicitly.
HISTORICAL_GAMES = {
    'ruby':3, 'sapphire':3, 'emerald':3, 'firered':3, 'leafgreen':3,
    'diamond':4, 'pearl':4, 'platinum':4, 'heartgold':4, 'soulsilver':4,
    'black':5, 'white':5, 'black-2':5, 'white-2':5,
    'x':6, 'y':6, 'omega-ruby':6, 'alpha-sapphire':6,
    'sun':7, 'moon':7, 'ultra-sun':7, 'ultra-moon':7,
}
EARLY_GAMES = {
    'red':1, 'blue':1, 'red-japan':1, 'blue-japan':1, 'green-japan':1, 'yellow':1,
    'gold':2, 'silver':2, 'crystal':2,
}
SV_GAMES = {'scarlet':9, 'violet':9}
STATS = {1: ('hp', 'HP'), 2: ('attack', 'Ataque'), 3: ('defense', 'Defesa'),
         4: ('special-attack', 'Ataque especial'), 5: ('special-defense', 'Defesa especial'), 6: ('speed', 'Velocidade')}


def _obter_ou_inserir(db, table, key, values, verify):
    # Identifiers are constants below; all domain values are bound parameters.
    where = ' AND '.join(f'{k}=?' for k in key)
    row = db.execute(f'SELECT * FROM {table} WHERE {where}', tuple(key.values())).fetchone()
    if row:
        if any(row[k] != values[k] for k in verify):
            raise ValueError(f'Conflito de curadoria em {table} ({key}); dados existentes preservados.')
        return row
    fields = list(key) + list(values)
    db.execute(f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})", tuple(key.values())+tuple(values.values()))
    return db.execute(f'SELECT * FROM {table} WHERE {where}', tuple(key.values())).fetchone()


def importar_mecanicas_swsh(db, data):
    """Conservative rules for Sword and Shield; explicit IDs never assume database IDs."""
    attrs = {}
    for number, (code, name) in STATS.items():
        attrs[number] = _obter_ou_inserir(db,'ATRIBUTO_BATALHA',{'codigo':code},{'nome':name},[])['id_atributo']
    names = {r['nature_id']: r['name'] for r in data['nature_names.csv'] if r['local_language_id']=='9'}
    for nature in data['natures.csv']:
        inc, dec = int(nature['increased_stat_id']), int(nature['decreased_stat_id'])
        neutral = inc == dec
        fields = {'atributo_aumentado': None if neutral else STATS[inc][0],
                  'atributo_reduzido': None if neutral else STATS[dec][0],
                  'estado_efeito': 'neutro' if neutral else 'modificador',
                  'fonte_url': NATURE_SOURCE, 'data_verificacao': DATE}
        _obter_ou_inserir(db,'NATUREZA',{'nome':names[nature['id']]},fields,
                           ['atributo_aumentado','atributo_reduzido','estado_efeito'])
    systems = {}
    for code, name in [('IV','Individual values'),('EV','Effort values')]:
        systems[code] = _obter_ou_inserir(db,'SISTEMA_ATRIBUTO',{'codigo':code}, {'nome':name}, [])['id_sistema_atributo']
    for game in ('Sword','Shield'):
        game_id = db.execute('SELECT id_jogo FROM JOGO WHERE nome=? COLLATE NOCASE',(game,)).fetchone()
        if not game_id:
            raise ValueError(f'Jogo {game} não encontrado; importação revertida.')
        values = {'usa_natureza':'sim','usa_habilidade':'sim','usa_nivel':'sim',
                  'nivel_minimo':1,'nivel_maximo':100,'fonte_url':OFFICIAL,'data_verificacao':DATE}
        mechanic = _obter_ou_inserir(db,'MECANICA_JOGO',{'id_jogo':game_id[0],'versao':'regras-gerais-documentadas'},values,
                                     ['usa_natureza','usa_habilidade','usa_nivel','nivel_minimo','nivel_maximo'])
        for code, max_attr, max_total, limit, source in [('IV',31,None,'nao_aplicavel',IV_SOURCE),('EV',252,510,'confirmado',EV_SOURCE)]:
            v = {'aplicabilidade':'aplicavel','valor_minimo':0,'valor_maximo_atributo':max_attr,
                 'valor_maximo_total':max_total,'limite_total_status':limit,'fonte_url':source,'data_verificacao':DATE}
            system = _obter_ou_inserir(db,'MECANICA_SISTEMA_ATRIBUTO',
                {'id_mecanica':mechanic['id_mecanica'],'id_sistema_atributo':systems[code]},v,
                ['aplicabilidade','valor_minimo','valor_maximo_atributo','valor_maximo_total','limite_total_status'])
            for attr in attrs.values():
                _obter_ou_inserir(db,'MECANICA_ATRIBUTO',{'id_mecanica_sistema_atributo':system['id_mecanica_sistema_atributo'],'id_atributo':attr},
                    {'aplicabilidade':'aplicavel','fonte_url':source,'data_verificacao':DATE},['aplicabilidade'])


def importar_mecanicas_historicas(db, data):
    """Explicitly selected core games, with the 255→252 EV change in Gen VI."""
    groups={r['id']:r for r in data['version_groups.csv']}
    versions={r['identifier']:r for r in data['versions.csv']}
    attrs=[db.execute('SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo=?',(code,)).fetchone()[0]
           for code,_ in STATS.values()]
    systems={code:db.execute('SELECT id_sistema_atributo FROM SISTEMA_ATRIBUTO WHERE codigo=?',(code,)).fetchone()[0]
             for code in ('IV','EV')}
    for code,generation in (HISTORICAL_GAMES | SV_GAMES).items():
        verification_date = SV_DATE if code in SV_GAMES else HISTORICAL_DATE
        version=versions.get(code)
        if not version or int(groups[version['version_group_id']]['generation_id'])!=generation:
            raise ValueError(f'Versão {code} não corresponde à fonte; carga revertida.')
        game=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(code,)).fetchone()
        if not game:
            raise ValueError(f'Jogo {code} não identificado; carga revertida.')
        values={'usa_natureza':'sim','usa_habilidade':'sim','usa_nivel':'sim',
                'nivel_minimo':1,'nivel_maximo':100,'fonte_url':ABILITY_SOURCE,'data_verificacao':verification_date}
        mechanic=_obter_ou_inserir(db,'MECANICA_JOGO',
            {'id_jogo':game[0],'versao':'regras-gerais-documentadas'},values,
            ['usa_natureza','usa_habilidade','usa_nivel','nivel_minimo','nivel_maximo'])
        for system_code,maximum,total,limit,source in (
            ('IV',31,None,'nao_aplicavel',IV_SOURCE),
            ('EV',255 if generation<=5 else 252,510,'confirmado',EV_SOURCE)):
            values={'aplicabilidade':'aplicavel','valor_minimo':0,'valor_maximo_atributo':maximum,
                    'valor_maximo_total':total,'limite_total_status':limit,'fonte_url':source,'data_verificacao':verification_date}
            system=_obter_ou_inserir(db,'MECANICA_SISTEMA_ATRIBUTO',
                {'id_mecanica':mechanic['id_mecanica'],'id_sistema_atributo':systems[system_code]},values,
                ['aplicabilidade','valor_minimo','valor_maximo_atributo','valor_maximo_total','limite_total_status'])
            for attr in attrs:
                _obter_ou_inserir(db,'MECANICA_ATRIBUTO',
                    {'id_mecanica_sistema_atributo':system['id_mecanica_sistema_atributo'],'id_atributo':attr},
                    {'aplicabilidade':'aplicavel','fonte_url':source,'data_verificacao':verification_date},['aplicabilidade'])


def importar_mecanicas_anteriores(db, data):
    """Independent DV and Stat Exp fields; HP DV is derived, Special is shared."""
    groups={r['id']:r for r in data['version_groups.csv']}
    versions={r['identifier']:r for r in data['versions.csv']}
    special=_obter_ou_inserir(db,'ATRIBUTO_BATALHA',{'codigo':'special'},{'nome':'Especial compartilhado'},['nome'])['id_atributo']
    attrs={code:db.execute('SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo=?',(code,)).fetchone()[0]
           for code in ('hp','attack','defense','speed')}
    attrs['special']=special
    systems={}
    for code,name,description in [
        ('DV','Determinant values','Quatro DVs independentes: ataque, defesa, velocidade e Especial compartilhado. O DV de HP é derivado deles.'),
        ('STAT_EXP','Stat Experience','Experiência de atributo para HP, ataque, defesa, velocidade e Especial compartilhado; não é o EV moderno.')]:
        systems[code]=_obter_ou_inserir(db,'SISTEMA_ATRIBUTO',{'codigo':code},
            {'nome':name,'descricao':description},['nome','descricao'])['id_sistema_atributo']
    for code,generation in EARLY_GAMES.items():
        version=versions.get(code)
        if not version or int(groups[version['version_group_id']]['generation_id'])!=generation:
            raise ValueError(f'Versão antiga {code} não corresponde à fonte; carga revertida.')
        game=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(code,)).fetchone()
        if not game:
            raise ValueError(f'Jogo {code} não identificado; carga revertida.')
        values={'usa_natureza':'nao','usa_habilidade':'nao','usa_nivel':'sim',
                'nivel_minimo':1,'nivel_maximo':100,'fonte_url':ABILITY_SOURCE,'data_verificacao':HISTORICAL_DATE}
        mechanic=_obter_ou_inserir(db,'MECANICA_JOGO',
            {'id_jogo':game[0],'versao':'regras-parciais-documentadas'},values,
            ['usa_natureza','usa_habilidade','usa_nivel','nivel_minimo','nivel_maximo'])
        for system_code,maximum,source,fields in [
            ('DV',15,IV_SOURCE,('attack','defense','speed','special')),
            ('STAT_EXP',65535,EV_SOURCE,('hp','attack','defense','speed','special'))]:
            limits={'aplicabilidade':'aplicavel','valor_minimo':0,'valor_maximo_atributo':maximum,
                    'valor_maximo_total':None,'limite_total_status':'nao_aplicavel',
                    'fonte_url':source,'data_verificacao':HISTORICAL_DATE}
            system=_obter_ou_inserir(db,'MECANICA_SISTEMA_ATRIBUTO',
                {'id_mecanica':mechanic['id_mecanica'],'id_sistema_atributo':systems[system_code]},limits,
                ['aplicabilidade','valor_minimo','valor_maximo_atributo','valor_maximo_total','limite_total_status'])
            for field in fields:
                _obter_ou_inserir(db,'MECANICA_ATRIBUTO',
                    {'id_mecanica_sistema_atributo':system['id_mecanica_sistema_atributo'],'id_atributo':attrs[field]},
                    {'aplicabilidade':'aplicavel','fonte_url':source,'data_verificacao':HISTORICAL_DATE},['aplicabilidade'])


def importar_mecanicas_lgpe(db):
    """IV e AV são distintos de EV; o estado de habilidades é não aplicável."""
    attrs=[db.execute('SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo=?',(code,)).fetchone()[0]
           for code,_ in STATS.values()]
    av=_obter_ou_inserir(db,'SISTEMA_ATRIBUTO',{'codigo':'AV'},
        {'nome':'Awakening Values','descricao':'Valores de despertar próprios de Let’s Go; não são EV.'},['nome','descricao'])
    ids={'AV':av['id_sistema_atributo']}
    for code in ('IV','EV'):
        ids[code]=db.execute('SELECT id_sistema_atributo FROM SISTEMA_ATRIBUTO WHERE codigo=?',(code,)).fetchone()[0]
    for game in ('lets-go-pikachu','lets-go-eevee'):
        row=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(game,)).fetchone()
        if not row:
            raise ValueError(f'Jogo {game} não identificado; carga revertida.')
        values={'usa_natureza':'sim','usa_habilidade':'nao','usa_nivel':'sim','nivel_minimo':1,'nivel_maximo':100,
                'fonte_url':LGPE_RULE_SOURCE,'data_verificacao':SV_DATE}
        mechanic=_obter_ou_inserir(db,'MECANICA_JOGO',{'id_jogo':row[0],'versao':'regras-parciais-documentadas'},values,
            ['usa_natureza','usa_habilidade','usa_nivel','nivel_minimo','nivel_maximo','fonte_url','data_verificacao'])
        for code,maximum,source in [('IV',31,IV_SOURCE),('AV',200,LGPE_RULE_SOURCE),('EV',None,LGPE_RULE_SOURCE)]:
            applicable='nao_aplicavel' if maximum is None else 'aplicavel'
            system_values={'aplicabilidade':applicable,'valor_minimo':None if maximum is None else 0,
                'valor_maximo_atributo':maximum,'valor_maximo_total':None,
                'limite_total_status':'nao_verificado' if maximum is None else 'nao_aplicavel',
                'fonte_url':source,'data_verificacao':SV_DATE}
            system=_obter_ou_inserir(db,'MECANICA_SISTEMA_ATRIBUTO',
                {'id_mecanica':mechanic['id_mecanica'],'id_sistema_atributo':ids[code]},system_values,
                ['aplicabilidade','valor_minimo','valor_maximo_atributo','valor_maximo_total','limite_total_status','fonte_url','data_verificacao'])
            for attr in attrs:
                _obter_ou_inserir(db,'MECANICA_ATRIBUTO',
                    {'id_mecanica_sistema_atributo':system['id_mecanica_sistema_atributo'],'id_atributo':attr},
                    {'aplicabilidade':applicable,'fonte_url':source,'data_verificacao':SV_DATE},
                    ['aplicabilidade','fonte_url','data_verificacao'])


def importar_regulamento_swsh(db, data, manifest):
    """Series 14, only default forms with verified encounters and a documented regional number."""
    dexes = {r['identifier']: r['id'] for r in data['pokedexes.csv']}
    limits = {dexes['galar']:400, dexes['isle-of-armor']:210, dexes['crown-tundra']:210}
    eligible = {int(r['species_id']) for r in data['pokemon_dex_numbers.csv']
                if r['pokedex_id'] in limits and int(r['pokedex_number']) <= limits[r['pokedex_id']]}
    for game in ('Sword','Shield'):
        mechanic = db.execute("""SELECT m.id_mecanica FROM MECANICA_JOGO m JOIN JOGO j USING(id_jogo)
            WHERE j.nome=? AND m.versao='regras-gerais-documentadas'""", (game,)).fetchone()
        rule = _obter_ou_inserir(db,'REGULAMENTO',
            {'id_mecanica':mechanic[0], 'codigo':'ranked-battles-series-14', 'versao':'season-36',
             'formato':'Ranked Battles', 'temporada':'November 2022'},
            {'nome':'Sword/Shield Ranked Battles Season 36', 'fonte_url':SERIES_14_SOURCE, 'data_verificacao':DATE},
            ['nome','fonte_url'])
        rows = db.execute("""SELECT d.id_dados_forma,e.numero_nacional FROM DADOS_FORMA_JOGO d
            JOIN FORMA f USING(id_forma) JOIN ESPECIE e USING(id_especie) JOIN JOGO j USING(id_jogo)
            WHERE j.nome=? AND f.forma_padrao=1 AND d.status_presenca='nativa' AND d.pode_ser_registrada='sim'
              AND d.fonte_url IN (?,?)""", (game,manifest['files']['encounters.csv.gz']['url'],DRAGAPULT_SOURCE)).fetchall()
        for sheet in rows:
            if sheet['numero_nacional'] not in eligible:
                continue
            condition = ('Espécie na faixa de uma Pokédex regional citada na regra; requer origem nos jogos '
                         'aceitos ou símbolo battle-ready. Outras condições do exemplar não foram verificadas.')
            _obter_ou_inserir(db,'ELEGIBILIDADE_FORMA_REGULAMENTO',
                {'id_regulamento':rule['id_regulamento'],'id_dados_forma':sheet['id_dados_forma']},
                {'status':'condicional','condicao':condition,'fonte_url':SERIES_14_SOURCE,'data_verificacao':DATE},
                ['status','condicao','fonte_url'])


def importar_dragapult(db):
    """The guide describes raising Dreepy into Dragapult in Sword and Shield."""
    for game in ('Sword','Shield'):
        row=db.execute("""SELECT f.id_forma,j.id_jogo FROM FORMA f JOIN ESPECIE e USING(id_especie)
            CROSS JOIN JOGO j WHERE e.numero_nacional=887 AND f.codigo_forma='dragapult'
            AND f.forma_padrao=1 AND j.nome=?""",(game,)).fetchone()
        if not row:
            raise ValueError('Forma ou jogo de Dragapult ausente; carga revertida.')
        existing=db.execute('SELECT * FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',tuple(row)).fetchone()
        if not existing:
            db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,
                motivo_registro,fonte_url,data_verificacao) VALUES (?,?,'nativa','sim',?,?,?)""",
                (*tuple(row),'Guia descreve treinar Dreepy para evoluir a Dragapult.',DRAGAPULT_SOURCE,DATE))


def importar_iniciais_sv(db):
    """A fonte oficial documenta a escolha de um destes três em cada versão."""
    method=db.execute("SELECT id_metodo FROM METODO_OBTENCAO WHERE nome='Presente no jogo'").fetchone()
    if not method:
        raise ValueError('Método de presente não encontrado; carga revertida.')
    for game in ('scarlet','violet'):
        for number,code in ((906,'sprigatito'),(909,'fuecoco'),(912,'quaxly')):
            row=db.execute("""SELECT f.id_forma,j.id_jogo FROM FORMA f JOIN ESPECIE e USING(id_especie)
                CROSS JOIN JOGO j WHERE e.numero_nacional=? AND f.codigo_forma=? AND f.forma_padrao=1
                AND j.codigo_versao_pokeapi=?""",(number,code,game)).fetchone()
            if not row:
                raise ValueError(f'Inicial {code} ou versão {game} ausente; carga revertida.')
            if db.execute('SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',tuple(row)).fetchone():
                continue  # Preserve a pre-existing context and its method curation.
            sheet=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,
                motivo_registro,fonte_url,data_verificacao) VALUES (?,?,'nativa','sim',?,?,?)""",
                (*tuple(row),'Um dos três primeiros parceiros escolhidos no início do jogo.',SV_STARTER_SOURCE,SV_DATE)).lastrowid
            db.execute("""INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao)
                VALUES(?,?,?,?,?)""",(sheet,method[0],'Escolha de um dos três primeiros parceiros.',SV_STARTER_SOURCE,SV_DATE))


def importar_evento_sv(db):
    """Evento encerrado de 18 a 20/10/2024, documentado para as duas versões."""
    method=_obter_ou_inserir(db,'METODO_OBTENCAO',{'nome':'Incursão Teracristal de evento'},
        {'descricao':'Encontro em incursão Teracristal de evento; consulte o período e as condições.'},['descricao'])
    condition=('Evento encerrado: 18/10/2024 00:00 a 20/10/2024 23:59 UTC; '
               'incursão de cinco estrelas em Paldea. Condições adicionais na fonte.')
    for game in ('scarlet','violet'):
        for number,code in ((874,'stonjourner'),(875,'eiscue-ice'),(936,'armarouge'),(937,'ceruledge')):
            row=db.execute("""SELECT f.id_forma,j.id_jogo FROM FORMA f JOIN ESPECIE e USING(id_especie)
                CROSS JOIN JOGO j WHERE e.numero_nacional=? AND f.codigo_forma=? AND f.forma_padrao=1
                AND f.estado_forma!='temporario' AND j.codigo_versao_pokeapi=?""",(number,code,game)).fetchone()
            if not row:
                raise ValueError(f'Forma {code} ou versão {game} ausente; carga revertida.')
            if db.execute('SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',tuple(row)).fetchone():
                continue
            sheet=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,
                motivo_registro,fonte_url,data_verificacao) VALUES (?,?,'nativa','sim',?,?,?)""",
                (*tuple(row),'Forma registrável no evento histórico especificado; não confirma disponibilidade atual.',SV_RAID_SOURCE,SV_DATE)).lastrowid
            db.execute("""INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao)
                VALUES(?,?,?,?,?)""",(sheet,method['id_metodo'],condition,SV_RAID_SOURCE,SV_DATE))


def importar_parceiros_lgpe(db):
    """Os parceiros iniciais são formas distintas de Pikachu e Eevee comuns."""
    method=db.execute("SELECT id_metodo FROM METODO_OBTENCAO WHERE nome='Presente no jogo'").fetchone()
    if not method:
        raise ValueError('Método de presente não encontrado; carga revertida.')
    for game,number,form in (('lets-go-pikachu',25,'pikachu-starter'),('lets-go-eevee',133,'eevee-starter')):
        row=db.execute("""SELECT f.id_forma,j.id_jogo FROM FORMA f JOIN ESPECIE e USING(id_especie)
            CROSS JOIN JOGO j WHERE e.numero_nacional=? AND f.codigo_forma=?
            AND f.estado_forma!='temporario' AND j.codigo_versao_pokeapi=?""",(number,form,game)).fetchone()
        if not row:
            raise ValueError(f'Parceiro {form} ou versão {game} ausente; carga revertida.')
        if db.execute('SELECT 1 FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',tuple(row)).fetchone():
            continue
        sheet=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,
            motivo_registro,fonte_url,data_verificacao) VALUES (?,?,'nativa','sim',?,?,?)""",
            (*tuple(row),'Parceiro inicial exclusivo desta versão, distinto da forma comum.',LGPE_PARTNER_SOURCE,SV_DATE)).lastrowid
        db.execute("""INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao)
            VALUES(?,?,?,?,?)""",(sheet,method[0],'Primeiro parceiro desta versão; não evolui nem pode ser transferido a outros jogos.',LGPE_PARTNER_SOURCE,SV_DATE))


def importar_disponibilidade_lgpe(db):
    """Complete default-form entries using the documented GO Park/device methods."""
    raw=LGPE_AVAILABILITY_FILE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=LGPE_AVAILABILITY_SHA256:
        raise ValueError('Referência de disponibilidade de Let’s Go alterada; carga revertida.')
    rows=list(csv.DictReader(raw.decode('utf-8').splitlines()))
    expected={*range(1,152),808,809}
    try:
        reference={int(row['numero_nacional']):row['metodo'] for row in rows}
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError('Referência de disponibilidade de Let’s Go inválida; carga revertida.') from exc
    if len(rows)!=153 or set(reference)!=expected or any(value not in ('go-park','poke-ball-plus') for value in reference.values()):
        raise ValueError('Referência de disponibilidade de Let’s Go incompleta ou duplicada; carga revertida.')
    if {n for n,method in reference.items() if method=='poke-ball-plus'}!={151}:
        raise ValueError('Método de Mew divergente na referência de Let’s Go; carga revertida.')

    methods={
        'go-park':_obter_ou_inserir(db,'METODO_OBTENCAO',{'nome':'Transferência via GO Park'},
            {'descricao':'Transferência unidirecional de Pokémon GO para Pokémon: Let’s Go.'},['descricao']),
        'poke-ball-plus':_obter_ou_inserir(db,'METODO_OBTENCAO',{'nome':'Presente do Poké Ball Plus'},
            {'descricao':'Presente especial de Mew vinculado ao acessório Poké Ball Plus.'},['descricao']),
    }
    for game in ('lets-go-pikachu','lets-go-eevee'):
        game_row=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(game,)).fetchone()
        if not game_row:
            raise ValueError(f'Jogo {game} não identificado; carga revertida.')
        for number,method_code in reference.items():
            form=db.execute("""SELECT f.id_forma FROM FORMA f JOIN ESPECIE e USING(id_especie)
                WHERE e.numero_nacional=? AND f.forma_padrao=1 AND f.estado_forma!='temporario'""",(number,)).fetchall()
            if len(form)!=1:
                raise ValueError(f'Forma padrão de número {number} ausente ou ambígua; carga revertida.')
            key=(form[0]['id_forma'],game_row[0])
            sheet=db.execute('SELECT id_dados_forma FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',key).fetchone()
            if not sheet:
                presence='nativa' if method_code=='poke-ball-plus' else 'transferivel'
                reason=('Mew é documentado via Poké Ball Plus.' if method_code=='poke-ball-plus' else
                        'Fonte documenta a compatibilidade via GO Park; não implica captura selvagem nesta versão.')
                identifier=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,
                    pode_ser_registrada,motivo_registro,fonte_url,data_verificacao)
                    VALUES(?,?,?, 'sim',?,?,?)""",(*key,presence,reason,LGPE_AVAILABILITY_SOURCE,LGPE_AVAILABILITY_DATE)).lastrowid
            else:
                identifier=sheet['id_dados_forma']
            method=methods[method_code]
            condition=('Transferência unidirecional de Pokémon GO pelo GO Park, disponível após chegar a Fuchsia City.'
                       if method_code=='go-park' else
                       'Presente especial de Mew via Poké Ball Plus; a fonte registra um Mew por acessório.')
            current=db.execute('SELECT * FROM METODO_FORMA_JOGO WHERE id_dados_forma=? AND id_metodo=?',
                               (identifier,method['id_metodo'])).fetchone()
            expected_values=(condition,LGPE_AVAILABILITY_SOURCE,LGPE_AVAILABILITY_DATE)
            if current:
                actual=(current['condicao'],current['fonte_url'],current['data_verificacao'])
                if actual!=expected_values:
                    raise ValueError(f'Conflito de curadoria no método de Let’s Go para espécie {number}; nenhum dado foi sobrescrito.')
            else:
                db.execute('''INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao)
                    VALUES(?,?,?,?,?)''',(identifier,method['id_metodo'],*expected_values))

    raw=LGPE_ALOLAN_FILE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=LGPE_ALOLAN_SHA256:
        raise ValueError('Referência das formas Alola em Let’s Go alterada; carga revertida.')
    alolan_rows=list(csv.DictReader(raw.decode('utf-8').splitlines()))
    try:
        alolan={int(row['numero_nacional']):row['codigo_forma'] for row in alolan_rows}
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError('Referência das formas Alola inválida; carga revertida.') from exc
    if len(alolan_rows)!=18 or alolan!=LGPE_ALOLAN_FORMS:
        raise ValueError('Referência das 18 formas Alola incompleta ou divergente; carga revertida.')
    park_method=methods['go-park']
    for game in ('lets-go-pikachu','lets-go-eevee'):
        game_id=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(game,)).fetchone()[0]
        for number,code in alolan.items():
            form=db.execute("""SELECT f.id_forma FROM FORMA f JOIN ESPECIE e USING(id_especie)
                WHERE e.numero_nacional=? AND f.codigo_forma=? AND f.estado_forma!='temporario'""",
                (number,code)).fetchone()
            if not form:
                raise ValueError(f'Forma Alola {code} ausente no snapshot; carga revertida.')
            key=(form['id_forma'],game_id)
            sheet=db.execute('SELECT id_dados_forma FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',key).fetchone()
            if not sheet:
                sheet_id=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,
                    pode_ser_registrada,motivo_registro,fonte_url,data_verificacao)
                    VALUES(?,?,'transferivel','sim',?,?,?)""",(*key,
                    'Forma Alola compatível via transferência de Pokémon GO pelo GO Park.',
                    LGPE_AVAILABILITY_SOURCE,LGPE_AVAILABILITY_DATE)).lastrowid
            else:
                sheet_id=sheet['id_dados_forma']
            method_key=(sheet_id,park_method['id_metodo'])
            existing=db.execute('SELECT * FROM METODO_FORMA_JOGO WHERE id_dados_forma=? AND id_metodo=?',method_key).fetchone()
            expected_values=('Transferência da forma Alola via GO Park; disponibilidade e exclusividade por versão não inferidas.',
                             LGPE_AVAILABILITY_SOURCE,LGPE_AVAILABILITY_DATE)
            if existing:
                if (existing['condicao'],existing['fonte_url'],existing['data_verificacao'])!=expected_values:
                    raise ValueError(f'Conflito de curadoria para a forma Alola {code}; dados preservados.')
            else:
                db.execute('''INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao)
                    VALUES(?,?,?,?,?)''',(sheet_id,park_method['id_metodo'],*expected_values))


def importar_perfis_dragapult(db):
    """Three explicit EV targets; no implied nature, ability or zeroes for other stats."""
    for game in ('Sword','Shield'):
        context=db.execute("""SELECT d.id_dados_forma,m.id_mecanica,ms.id_mecanica_sistema_atributo
            FROM DADOS_FORMA_JOGO d JOIN FORMA f USING(id_forma) JOIN JOGO j USING(id_jogo)
            JOIN MECANICA_JOGO m USING(id_jogo) JOIN MECANICA_SISTEMA_ATRIBUTO ms USING(id_mecanica)
            JOIN SISTEMA_ATRIBUTO s USING(id_sistema_atributo)
            WHERE j.nome=? AND f.codigo_forma='dragapult' AND d.fonte_url=?
            AND m.versao='regras-gerais-documentadas' AND s.codigo='EV'""",(game,DRAGAPULT_SOURCE)).fetchone()
        if not context:
            continue  # Preserve a pre-existing sheet from another source without adopting it.
        key={'id_dados_forma':context['id_dados_forma'],'id_mecanica':context['id_mecanica'],
             'nome_perfil':'Dragapult ofensivo — exemplo VGC', 'tipo_perfil':'referencia_competitiva'}
        values={'descricao':'Exemplo histórico do guia VGC: 252 EV em ataque, 252 em velocidade e 4 em HP. Outros alvos não foram especificados.',
                'fonte_url':DRAGAPULT_SOURCE,'data_verificacao':DATE,'versao_fonte':'Sword/Shield, consultado em 2026-11-14'}
        profile=_obter_ou_inserir(db,'PERFIL_ANALISE',key,values,['descricao','fonte_url','versao_fonte'])
        for code, target in [('attack',252),('speed',252),('hp',4)]:
            attr=db.execute('SELECT id_atributo FROM ATRIBUTO_BATALHA WHERE codigo=?',(code,)).fetchone()[0]
            _obter_ou_inserir(db,'VALOR_PERFIL_ANALISE',
                {'id_perfil':profile['id_perfil'],'id_mecanica_sistema_atributo':context['id_mecanica_sistema_atributo'],'id_atributo':attr},
                {'estado':'conhecido','valor_alvo':target},['estado','valor_alvo'])


def importar_transformacoes_lgpe(db):
    """Contextualize Mega forms as temporary battle transformations, never specimens."""
    raw=LGPE_MEGA_FILE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=LGPE_MEGA_SHA256:
        raise ValueError('Referência das Megaevoluções de Let’s Go alterada; carga revertida.')
    rows=list(csv.DictReader(raw.decode('utf-8').splitlines()))
    try:
        reference=[(int(row['numero_nacional']),row['codigo_forma']) for row in rows]
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError('Referência das Megaevoluções inválida; carga revertida.') from exc
    expected={(number,code) for number,codes in LGPE_MEGA_FORMS.items() for code in codes}
    if len(rows)!=15 or len(set(reference))!=15 or set(reference)!=expected:
        raise ValueError('Referência das 15 formas Mega de Kanto incompleta ou divergente; carga revertida.')
    for game in ('lets-go-pikachu','lets-go-eevee'):
        game_id=db.execute('SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=?',(game,)).fetchone()[0]
        for number,mega_code in reference:
            mega=db.execute("""SELECT f.id_forma FROM FORMA f JOIN ESPECIE e USING(id_especie)
                WHERE e.numero_nacional=? AND f.codigo_forma=? AND f.estado_forma='temporario'""",
                (number,mega_code)).fetchone()
            base=db.execute("""SELECT id_forma FROM FORMA WHERE id_especie=(SELECT id_especie FROM FORMA WHERE id_forma=?)
                AND forma_padrao=1""",(mega['id_forma'],)).fetchone() if mega else None
            if not mega or not base:
                raise ValueError(f'Forma Mega ou forma-base ausente para {mega_code}; carga revertida.')
            base_sheet=db.execute('SELECT id_dados_forma FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',
                                  (base['id_forma'],game_id)).fetchone()
            if not base_sheet:
                raise ValueError(f'Ficha-base de {mega_code} não está documentada em {game}; carga revertida.')
            destination=db.execute('SELECT id_dados_forma FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?',
                                   (mega['id_forma'],game_id)).fetchone()
            if not destination:
                destination_id=db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,
                    pode_ser_registrada,motivo_registro,fonte_url,data_verificacao)
                    VALUES(?,?,'nativa','nao',?,?,?)""",(mega['id_forma'],game_id,
                    'Forma temporária de batalha; não pode ser capturada ou mantida como exemplar separado.',
                    LGPE_MEGA_SOURCE,LGPE_AVAILABILITY_DATE)).lastrowid
            else:
                destination_id=destination['id_dados_forma']
                row=db.execute('SELECT status_presenca,pode_ser_registrada,fonte_url,data_verificacao FROM DADOS_FORMA_JOGO WHERE id_dados_forma=?',(destination_id,)).fetchone()
                if tuple(row)!=('nativa','nao',LGPE_MEGA_SOURCE,LGPE_AVAILABILITY_DATE):
                    raise ValueError(f'Ficha da forma Mega {mega_code} diverge da transformação curada; dados preservados.')
            condition='Uma vez por batalha, com Key Stone e Mega Stone correspondente; a forma retorna ao encerrar a batalha.'
            item='Key Stone e Mega Stone correspondente'
            observation='Estado de transformação de batalha; não representa captura, transferência ou registro independente.'
            key=(base_sheet['id_dados_forma'],destination_id,'Mega Evolution',condition)
            existing=db.execute("""SELECT * FROM TRANSFORMACAO_FORMA WHERE id_dados_forma_origem=?
                AND id_dados_forma_destino=? AND tipo_transformacao=? AND condicao=?""",key).fetchone()
            values=(1,item,observation,LGPE_MEGA_SOURCE,LGPE_AVAILABILITY_DATE)
            if existing:
                if tuple(existing[k] for k in ('temporaria','item_requerido','observacao','fonte_url','data_verificacao'))!=values:
                    raise ValueError(f'Conflito na transformação Mega {mega_code}; dados preservados.')
            else:
                db.execute("""INSERT INTO TRANSFORMACAO_FORMA(id_dados_forma_origem,id_dados_forma_destino,
                    tipo_transformacao,temporaria,condicao,item_requerido,observacao,fonte_url,data_verificacao)
                    VALUES(?,?, 'Mega Evolution',?,?,?,?,?,?)""",(base_sheet['id_dados_forma'],destination_id,
                    1,condition,item,observation,LGPE_MEGA_SOURCE,LGPE_AVAILABILITY_DATE))
