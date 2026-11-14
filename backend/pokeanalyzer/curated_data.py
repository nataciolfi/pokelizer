"""Explicitly sourced mechanics for the two named games; no generation-wide inference."""

OFFICIAL = 'https://www.pokemon.com/us/strategy/train-raid-and-hatch-pokemon-to-breed-victories-in-pokemon-sword-and-pokemon-shield'
IV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Individual_values'
EV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Effort_values'
NATURE_SOURCE = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/8a92bfa7dab2f12b84b5d151562f9857c133ff30/data/v2/csv/natures.csv'
DATE = '2026-11-14'
SERIES_14_SOURCE = 'https://www.pokemon.com/us/pokemon-news/pokemon-sword-and-pokemon-shield-ranked-battles-november-2022-season-season-36/'
DRAGAPULT_SOURCE = 'https://www.vgcguide.com/ev-training'
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
