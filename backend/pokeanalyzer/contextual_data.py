"""PokéAPI data at a pinned generation, limited to independently confirmed Sw/Sh sheets."""
from collections import defaultdict
from .curated_data import _obter_ou_inserir, DATE, DRAGAPULT_SOURCE


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


def importar_contextos_swsh(db, data, manifest):
    """Never overwrite existing curated values, types, abilities or their provenance."""
    source = manifest['source_url']
    encounter_source = manifest['files']['encounters.csv.gz']['url']
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
    past_stats = defaultdict(lambda: defaultdict(list))
    for r in data['pokemon_stats_past.csv']:
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
    sheets = db.execute("""SELECT d.*,e.numero_nacional,f.codigo_forma FROM DADOS_FORMA_JOGO d
        JOIN FORMA f USING(id_forma) JOIN ESPECIE e USING(id_especie) JOIN JOGO j USING(id_jogo)
        WHERE j.nome IN ('Sword','Shield') AND d.fonte_url IN (?,?)""", (encounter_source,DRAGAPULT_SOURCE)).fetchall()
    for sheet in sheets:
        pid = by_form.get((sheet['numero_nacional'],sheet['codigo_forma']))
        if pid is None:
            raise ValueError('Forma contextual não corresponde ao snapshot; carga revertida.')
        selected_types = current_types[pid]
        eligible = [g for g in past_types[pid] if g >= 8]
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
            db.execute("UPDATE DADOS_FORMA_JOGO SET status_tipos='aplicavel',fonte_tipos=?,data_verificacao_tipos=? WHERE id_dados_forma=?",(source,DATE,sheet['id_dados_forma']))
        stats = _historical_rows(current_stats[pid],past_stats[pid],8,'base_stat')
        if all(sheet[column] is None for column in attrs.values()) and sheet['fonte_estatisticas'] is None and set(stats)==set(attrs):
            db.execute('UPDATE DADOS_FORMA_JOGO SET '+','.join(column+'=?' for column in attrs.values())+',fonte_estatisticas=?,data_verificacao_estatisticas=? WHERE id_dados_forma=?',
                tuple(int(stats[n]) for n in attrs)+(source,DATE,sheet['id_dados_forma']))
        has_abilities = db.execute('SELECT 1 FROM HABILIDADE_FORMA_JOGO WHERE id_dados_forma=? LIMIT 1',(sheet['id_dados_forma'],)).fetchone()
        if not has_abilities:
            abilities = _historical_rows(current_abilities[pid],past_abilities[pid],8,'ability_id')
            for slot, ability_id in sorted(abilities.items()):
                if not ability_id:
                    continue
                name = ability_names.get(ability_id, ability_codes.get(ability_id))
                if not name:
                    raise ValueError('Habilidade sem nome na fonte; carga revertida.')
                ability = _obter_ou_inserir(db,'HABILIDADE',{'nome':name},{},[])
                db.execute('''INSERT INTO HABILIDADE_FORMA_JOGO(id_dados_forma,id_habilidade,slot,fonte_url,data_verificacao)
                    VALUES(?,?,?,?,?)''',(sheet['id_dados_forma'],ability['id_habilidade'],'slot-'+slot,source,DATE))
