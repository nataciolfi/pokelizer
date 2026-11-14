"""Explicitly sourced mechanics for the two named games; no generation-wide inference."""

OFFICIAL = 'https://www.pokemon.com/us/strategy/train-raid-and-hatch-pokemon-to-breed-victories-in-pokemon-sword-and-pokemon-shield'
IV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Individual_values'
EV_SOURCE = 'https://bulbapedia.bulbagarden.net/wiki/Effort_values'
NATURE_SOURCE = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/8a92bfa7dab2f12b84b5d151562f9857c133ff30/data/v2/csv/natures.csv'
DATE = '2026-11-14'
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
