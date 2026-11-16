"""Generation histories for independently sourced, unambiguous game sheets."""
from collections import defaultdict
from .curated_data import _obter_ou_inserir, DRAGAPULT_SOURCE, SV_STARTER_SOURCE, SV_DATE

CONTEXT_DATE = '2026-11-15'
# Groups with the six-stat system and/or abilities. Generation I has one
# Special stat; Let's Go and Legends: Arceus have no abilities in battle.
STANDARD_GROUPS = {
    'gold-silver', 'crystal', 'ruby-sapphire', 'emerald', 'firered-leafgreen',
    'diamond-pearl', 'platinum', 'heartgold-soulsilver', 'black-white',
    'black-2-white-2', 'x-y', 'omega-ruby-alpha-sapphire', 'sun-moon',
    'ultra-sun-ultra-moon', 'sword-shield', 'the-isle-of-armor', 'the-crown-tundra', 'scarlet-violet',
}
TYPE_ONLY_GROUPS = {'red-green-japan', 'blue-japan', 'red-blue', 'yellow'}


def _historical_rows(current, past, generation, value_field):
    """Apply the first documented previous value whose last generation includes this one."""
    effective = {key: row[value_field] for key, row in current.items()}
    candidates = defaultdict(list)
    for key, rows in past.items():
        candidates[key].extend(r for r in rows if int(r['generation_id']) >= generation)
    for key, rows in candidates.items():
        if rows:
            effective[key] = min(rows, key=lambda r:int(r['generation_id']))[value_field]
    return effective


def importar_contextos_por_geracao(db, data, manifest):
    """Never overwrite existing curated values, types, abilities or their provenance."""
    source = manifest['source_url']
    encounter_source = manifest['files']['encounters.csv.gz']['url']
    groups = {r['id']:r for r in data['version_groups.csv']}
    versions = {v['identifier']:groups[v['version_group_id']] for v in data['versions.csv']}
    pokemon = {r['id']:r for r in data['pokemon.csv']}
    by_form = {(int(pokemon[f['pokemon_id']]['species_id']), f['identifier']):f['pokemon_id']
               for f in data['pokemon_forms.csv']}
    current_types = defaultdict(dict)
    for r in data['pokemon_types.csv']:
        current_types[r['pokemon_id']][r['slot']] = r
    past_types = defaultdict(lambda: defaultdict(list))
    for r in data['pokemon_types_past.csv']:
        past_types[r['pokemon_id']][int(r['generation_id'])].append(r)
    current_stats = defaultdict(dict)
    for r in data['pokemon_stats.csv']:
        if r['stat_id'] in {'1','2','3','4','5','6'}:
            current_stats[r['pokemon_id']][r['stat_id']] = r
    special_ids=[r['id'] for r in data['stats.csv'] if r['identifier']=='special']
    if len(special_ids)!=1:
        raise ValueError('Identificador de Especial ausente ou ambíguo no snapshot; carga revertida.')
    first_special={}
    past_stats = defaultdict(lambda: defaultdict(list))
    for r in data['pokemon_stats_past.csv']:
        if r['stat_id']==special_ids[0] and r['generation_id']=='1':
            if r['pokemon_id'] in first_special:
                raise ValueError('Especial histórico duplicado no snapshot; carga revertida.')
            first_special[r['pokemon_id']]=r['base_stat']
        if r['stat_id'] in {'1','2','3','4','5','6'}:
            past_stats[r['pokemon_id']][r['stat_id']].append(r)
    current_abilities = defaultdict(dict)
    for r in data['pokemon_abilities.csv']:
        current_abilities[r['pokemon_id']][r['slot']] = r
    past_abilities = defaultdict(lambda: defaultdict(list))
    for r in data['pokemon_abilities_past.csv']:
        past_abilities[r['pokemon_id']][r['slot']].append(r)
    type_names = {r['type_id']:r['name'] for r in data['type_names.csv'] if r['local_language_id']=='9'}
    ability_names = {r['ability_id']:r['name'] for r in data['ability_names.csv'] if r['local_language_id']=='9'}
    ability_codes = {r['id']:r['identifier'] for r in data['abilities.csv']}
    attrs = {'1':'hp_base','2':'ataque_base','3':'defesa_base','4':'ataque_especial_base','5':'defesa_especial_base','6':'velocidade_base'}
    sheets = db.execute("""SELECT d.*,e.numero_nacional,f.codigo_forma,j.codigo_versao_pokeapi FROM DADOS_FORMA_JOGO d
        JOIN FORMA f USING(id_forma) JOIN ESPECIE e USING(id_especie) JOIN JOGO j USING(id_jogo)
        WHERE d.fonte_url IN (?,?,?)""", (encounter_source,DRAGAPULT_SOURCE,SV_STARTER_SOURCE)).fetchall()
    for sheet in sheets:
        context_date = SV_DATE if sheet['fonte_url'] == SV_STARTER_SOURCE else CONTEXT_DATE
        group = versions.get(sheet['codigo_versao_pokeapi'])
        if not group or group['identifier'] not in STANDARD_GROUPS | TYPE_ONLY_GROUPS:
            continue
        generation = int(group['generation_id'])
        pid = by_form.get((sheet['numero_nacional'],sheet['codigo_forma']))
        if pid is None:
            raise ValueError('Forma contextual não corresponde ao snapshot; carga revertida.')
        selected_types = current_types[pid]
        eligible = [g for g in past_types[pid] if g >= generation]
        if eligible:
            selected_types = {r['slot']:r for r in past_types[pid][min(eligible)]}
        has_types = db.execute('SELECT 1 FROM TIPO_FORMA_JOGO WHERE id_dados_forma=? LIMIT 1',(sheet['id_dados_forma'],)).fetchone()
        if sheet['status_tipos']=='nao_verificado' and not has_types and sheet['fonte_tipos'] is None and selected_types:
            for slot, item in sorted(selected_types.items()):
                name = type_names.get(item['type_id'])
                if not name or int(slot) not in (1,2):
                    raise ValueError('Tipo ou slot inesperado no snapshot; carga revertida.')
                kind = _obter_ou_inserir(db,'TIPO',{'nome_tipo':name},{},[])
                db.execute('INSERT INTO TIPO_FORMA_JOGO(id_dados_forma,id_tipo,posicao) VALUES(?,?,?)',(sheet['id_dados_forma'],kind['id_tipo'],int(slot)))
            db.execute("UPDATE DADOS_FORMA_JOGO SET status_tipos='aplicavel',fonte_tipos=?,data_verificacao_tipos=? WHERE id_dados_forma=?",(source,context_date,sheet['id_dados_forma']))
        # Generation I has a single sourced Special, never two modern fields.
        if group['identifier'] in TYPE_ONLY_GROUPS:
            old_stats=_historical_rows(current_stats[pid],past_stats[pid],generation,'base_stat')
            old_attrs={'1':'hp_base','2':'ataque_base','3':'defesa_base','6':'velocidade_base'}
            if (all(sheet[column] is None for column in attrs.values()) and sheet['especial_base'] is None
                and sheet['fonte_estatisticas'] is None and all(k in old_stats for k in old_attrs) and pid in first_special):
                db.execute('UPDATE DADOS_FORMA_JOGO SET '+','.join(column+'=?' for column in old_attrs.values())+
                           ',especial_base=?,fonte_estatisticas=?,data_verificacao_estatisticas=? WHERE id_dados_forma=?',
                    tuple(int(old_stats[k]) for k in old_attrs)+(int(first_special[pid]),source,context_date,sheet['id_dados_forma']))
            continue
        if group['identifier'] not in STANDARD_GROUPS:
            continue
        stats = _historical_rows(current_stats[pid],past_stats[pid],generation,'base_stat')
        if all(sheet[column] is None for column in attrs.values()) and sheet['especial_base'] is None and sheet['fonte_estatisticas'] is None and set(stats)==set(attrs):
            db.execute('UPDATE DADOS_FORMA_JOGO SET '+','.join(column+'=?' for column in attrs.values())+',fonte_estatisticas=?,data_verificacao_estatisticas=? WHERE id_dados_forma=?',
                tuple(int(stats[n]) for n in attrs)+(source,context_date,sheet['id_dados_forma']))
        # Generations I and II have no abilities; omission here does not mean zero.
        if generation < 3:
            continue
        has_abilities = db.execute('SELECT 1 FROM HABILIDADE_FORMA_JOGO WHERE id_dados_forma=? LIMIT 1',(sheet['id_dados_forma'],)).fetchone()
        if not has_abilities:
            abilities = _historical_rows(current_abilities[pid],past_abilities[pid],generation,'ability_id')
            for slot, ability_id in sorted(abilities.items()):
                if not ability_id:
                    continue
                name = ability_names.get(ability_id, ability_codes.get(ability_id))
                if not name:
                    raise ValueError('Habilidade sem nome na fonte; carga revertida.')
                ability = _obter_ou_inserir(db,'HABILIDADE',{'nome':name},{},[])
                db.execute('''INSERT INTO HABILIDADE_FORMA_JOGO(id_dados_forma,id_habilidade,slot,condicao,fonte_url,data_verificacao)
                    VALUES(?,?,?,?,?,?)''',(sheet['id_dados_forma'],ability['id_habilidade'],'slot-'+slot,
                    'Habilidade potencial na geração; obtenção nesta versão não comprovada.',source,context_date))
