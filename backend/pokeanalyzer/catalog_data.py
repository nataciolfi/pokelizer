"""Pinned upstream identities. Game mechanics are never inferred from global rows."""
import csv
import hashlib
import gzip
from collections import Counter, defaultdict
import json
from pathlib import Path
from .db import get_db, transaction

SNAPSHOT = Path(__file__).resolve().parents[1] / 'data' / 'pokeapi'

# Source identifiers reviewed against encounter_method_prose.csv. NPC trades,
# distributions, raids and shadow Pokémon need separate semantics.
WILD_METHODS = frozenset({
    'walk','old-rod','good-rod','super-rod','surf','rock-smash','headbutt',
    'dark-grass','grass-spots','cave-spots','bridge-spots','super-rod-spots',
    'surf-spots','yellow-flowers','purple-flowers','red-flowers','rough-terrain',
    'headbutt-low','headbutt-normal','headbutt-high','seaweed','roaming-grass',
    'roaming-water','feebas-tile-fishing','island-scan','sos','bubbling-spots',
    'berry-trees','sos-from-bubbling-spot','overworld','overworld-water',
    'overworld-flying','overworld-special','overworld-flying-special',
    'overworld-water-special','horde','pokespot','hidden-grotto','honey-tree',
    'overworld-dirt','wanderer','wanderer-water','chase-water','trash-can-ambush',
    'rustling-bush-ambush','ceiling-ambush','ground-ambush','sky-ambush',
})
METHOD_GROUPS = {
    'Encontro selvagem': WILD_METHODS,
    'Presente no jogo': frozenset({'gift'}),
    'Ovo recebido no jogo': frozenset({'gift-egg'}),
}


def ler_snapshot(directory=SNAPSHOT):
    manifest = json.loads((directory / 'manifest.json').read_text())
    tables = {}
    for name, meta in manifest['files'].items():
        raw = (directory / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != meta['sha256']:
            raise ValueError(f'Snapshot alterado: {name}. Nenhum dado importado.')
        if name.endswith('.csv.gz'):
            raw = gzip.decompress(raw)
            if hashlib.sha256(raw).hexdigest() != meta['raw_sha256']:
                raise ValueError(f'Conteúdo descompactado alterado: {name}.')
            tables[name.removesuffix('.gz')] = list(csv.DictReader(raw.decode('utf-8').splitlines()))
        elif name.endswith('.csv'):
            tables[name] = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    return manifest, tables


def importar_catalogo(directory=SNAPSHOT):
    manifest, data = ler_snapshot(directory)
    db = get_db()
    source = manifest['source_url']
    date = manifest['retrieved_at']
    names = {int(r['pokemon_species_id']): r['name'] for r in data['pokemon_species_names.csv'] if r['local_language_id'] == '9'}
    pokemon = {r['id']: r for r in data['pokemon.csv']}
    groups = {r['id']: r for r in data['version_groups.csv']}
    game_names = {r['version_id']: r['name'] for r in data['version_names.csv'] if r['local_language_id'] == '9'}
    game_name_counts = Counter(game_names.get(r['id'], r['identifier']).casefold() for r in data['versions.csv'])
    with transaction(db):
        for r in data['pokemon_species.csv']:
            number = int(r['id'])
            name = names.get(number, r['identifier'])
            existing = db.execute('SELECT * FROM ESPECIE WHERE numero_nacional=?', (number,)).fetchone()
            if existing and (existing['nome_en'] != name or existing['fonte_url'] != source):
                raise ValueError(f'Conflito em espécie {number}; catálogo existente preservado, requer curadoria explícita.')
            if not existing:
                # nome_pt is the required display name in the inherited schema; no translation claimed.
                db.execute('INSERT INTO ESPECIE(numero_nacional,nome_pt,nome_en,geracao_origem,fonte_url,data_verificacao) VALUES(?,?,?,?,?,?)',
                           (number, name, name, int(r['generation_id']), source, date))
        for r in data['pokemon_forms.csv']:
            p = pokemon[r['pokemon_id']]
            species = db.execute('SELECT id_especie FROM ESPECIE WHERE numero_nacional=?', (int(p['species_id']),)).fetchone()[0]
            code = r['identifier']
            default = int(p['is_default'] == '1' and r['is_default'] == '1')
            category = 'padrao' if default else 'nao_verificada'
            existing = db.execute('SELECT * FROM FORMA WHERE id_especie=? AND codigo_forma=?', (species, code)).fetchone()
            if existing and (existing['fonte_url'] != source or existing['forma_padrao'] != default or existing['categoria'] != category):
                raise ValueError(f'Conflito em forma {code}; importação revertida.')
            if not existing:
                db.execute('INSERT INTO FORMA(id_especie,codigo_forma,nome_forma,forma_padrao,estado_forma,fonte_url,data_verificacao,categoria) VALUES(?,?,?,?,?,?,?,?)',
                    (species, code, code, default, 'temporario' if r['is_battle_only']=='1' else 'nao_verificado', source, date, category))
        for r in data['versions.csv']:
            name = game_names.get(r['id'], r['identifier'])
            ambiguous = game_name_counts[name.casefold()] > 1
            display = f"{name} ({r['identifier']})" if ambiguous else name
            generation = int(groups[r['version_group_id']]['generation_id'])
            existing = db.execute('SELECT * FROM JOGO WHERE codigo_versao_pokeapi=? COLLATE NOCASE', (r['identifier'],)).fetchone()
            if existing:
                if existing['fonte_url'] != source or existing['geracao'] != generation:
                    raise ValueError(f"Conflito na versão {r['identifier']}; catálogo existente preservado.")
                continue
            named = db.execute('SELECT * FROM JOGO WHERE nome=? COLLATE NOCASE', (display,)).fetchone()
            if named:
                # Only a unique old source name can be mapped without guessing.
                if ambiguous or named['fonte_url'] != source or named['geracao'] != generation or named['codigo_versao_pokeapi'] is not None:
                    raise ValueError(f'Conflito em jogo {display}; catálogo existente preservado.')
                db.execute('UPDATE JOGO SET codigo_versao_pokeapi=? WHERE id_jogo=?', (r['identifier'], named['id_jogo']))
            else:
                db.execute('INSERT INTO JOGO(nome,geracao,fonte_url,data_verificacao,codigo_versao_pokeapi) VALUES(?,?,?,?,?)',
                    (display, generation, source, date, r['identifier']))
        importar_encontros(db, data, manifest)
        from .curated_data import importar_mecanicas_swsh, importar_mecanicas_historicas, importar_mecanicas_anteriores, importar_dragapult, importar_iniciais_sv, importar_evento_sv
        importar_mecanicas_swsh(db, data)
        importar_mecanicas_historicas(db, data)
        importar_mecanicas_anteriores(db, data)
        importar_dragapult(db)
        importar_iniciais_sv(db)
        importar_evento_sv(db)
        from .contextual_data import importar_contextos_por_geracao
        importar_contextos_por_geracao(db, data, manifest)
        from .curated_data import importar_regulamento_swsh
        importar_regulamento_swsh(db, data, manifest)
        from .curated_data import importar_perfis_dragapult
        importar_perfis_dragapult(db)
        if db.execute('PRAGMA foreign_key_check').fetchone():
            raise ValueError('Snapshot violou integridade; carga revertida.')
    return cobertura(directory)



def importar_encontros(db, data, manifest):
    """Only unambiguous, independently registrable wild encounters, not game indices."""
    forms_by_pokemon = {}
    for row in data['pokemon_forms.csv']:
        forms_by_pokemon.setdefault(row['pokemon_id'], []).append(row)
    one_form = {pid: rows[0] for pid, rows in forms_by_pokemon.items()
                if len(rows) == 1 and rows[0]['is_default'] == '1' and rows[0]['is_battle_only'] == '0'}
    pokemon = {r['id']: r for r in data['pokemon.csv']}
    versions = {v['id']: v['identifier'] for v in data['versions.csv']}
    source = manifest['files']['encounters.csv.gz']['url']
    date = manifest['files']['encounters.csv.gz']['retrieved_at']
    # Use reviewed identifiers, never label gifts or eggs as wild. NPC trades,
    # distributions, raids and snagging are intentionally excluded.
    group_for = {identifier:group for group,identifiers in METHOD_GROUPS.items() for identifier in identifiers}
    methods = {r['id']:r['identifier'] for r in data['encounter_methods.csv'] if r['identifier'] in group_for}
    if set(methods.values()) != set(group_for) or len(methods) != len(group_for):
        raise ValueError('Métodos ausentes ou ambíguos na fonte; carga revertida.')
    prose = {r['encounter_method_id']:r['name'] for r in data['encounter_method_prose.csv'] if r['local_language_id']=='9'}
    if not set(methods).issubset(prose):
        raise ValueError('Descrição de método ausente na fonte; carga revertida.')
    selected_slots = {r['id']: (r['version_group_id'],r['encounter_method_id']) for r in data['encounter_slots.csv'] if r['encounter_method_id'] in methods}
    version_groups = {r['id']: r['version_group_id'] for r in data['versions.csv']}
    # Absence of a matching encounter never implies absence in the game.
    pairs = defaultdict(lambda: defaultdict(set))
    for encounter in data['encounters.csv']:
        pid,vid,slot = encounter['pokemon_id'],encounter['version_id'],selected_slots.get(encounter['encounter_slot_id'])
        if pid in one_form and vid in versions and slot and slot[0] == version_groups[vid]:
            pairs[(pid,vid)][group_for[methods[slot[1]]]].add(slot[1])
    descriptions = {
        'Encontro selvagem':'Encontro selvagem documentado na fonte; condições variam por local.',
        'Presente no jogo':'Recebimento documentado na fonte; condições e local variam.',
        'Ovo recebido no jogo':'Ovo recebido no jogo, com espécie documentada na fonte; condições e local variam.',
    }
    method_ids={}
    for name,description in descriptions.items():
        method = db.execute('SELECT id_metodo,descricao FROM METODO_OBTENCAO WHERE nome=? COLLATE NOCASE',(name,)).fetchone()
        if not method:
            method = db.execute('INSERT INTO METODO_OBTENCAO(nome,descricao) VALUES(?,?)',(name,description))
            method_ids[name]=method.lastrowid
        else:
            if method['descricao'] != description:
                raise ValueError(f'Conflito no método {name}; curadoria existente preservada.')
            method_ids[name]=method[0]
    for pid, vid in sorted(pairs, key=lambda p: (int(p[1]), int(p[0]))):
        row = one_form[pid]
        existing_form = db.execute("SELECT f.id_forma FROM FORMA f JOIN ESPECIE e USING(id_especie) WHERE e.numero_nacional=? AND f.codigo_forma=?", (int(pokemon[pid]['species_id']), row['identifier'])).fetchone()
        game = db.execute("SELECT id_jogo FROM JOGO WHERE codigo_versao_pokeapi=? COLLATE NOCASE", (versions[vid],)).fetchone()
        if not existing_form or not game:
            raise ValueError('Forma ou jogo da fonte não encontrado; carga revertida.')
        current = db.execute("SELECT * FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?", (existing_form[0],game[0])).fetchone()
        if current:
            # Curated or conflicting facts are never replaced. They remain visible in the coverage report.
            continue
        cursor = db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,fonte_url,data_verificacao)
                                VALUES(?,?,'nativa','sim',?,?)""", (existing_form[0],game[0],source,date))
        for group,ids in sorted(pairs[(pid,vid)].items()):
            condition = ('Métodos descritos pela fonte: ' + '; '.join(sorted(prose[mid] for mid in ids)) +
                         '. Local, período e demais condições dependem do jogo e não foram detalhados aqui.')
            db.execute("INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,condicao,fonte_url,data_verificacao) VALUES(?,?,?,?,?)",
                       (cursor.lastrowid,method_ids[group],condition,source,date))

def cobertura(directory=SNAPSHOT):
    from .curated_data import DRAGAPULT_SOURCE, SV_STARTER_SOURCE, SV_RAID_SOURCE
    manifest, data = ler_snapshot(directory)
    db = get_db()
    counts = {t: db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in
        ('ESPECIE','FORMA','JOGO','DADOS_FORMA_JOGO','MECANICA_JOGO','REGULAMENTO','ELEGIBILIDADE_FORMA_REGULAMENTO')}
    matched = {
        'especies': db.execute('SELECT count(*) FROM ESPECIE WHERE fonte_url=?', (manifest['source_url'],)).fetchone()[0],
        'formas': db.execute('SELECT count(*) FROM FORMA WHERE fonte_url=?', (manifest['source_url'],)).fetchone()[0]}
    games = [dict(row) for row in db.execute("""SELECT j.nome,j.codigo_versao_pokeapi,j.geracao,
        COUNT(d.id_dados_forma) AS fichas,
        SUM(CASE WHEN d.fonte_tipos IS NOT NULL THEN 1 ELSE 0 END) AS tipos_com_fonte,
        SUM(CASE WHEN d.fonte_estatisticas IS NOT NULL AND d.hp_base IS NOT NULL AND d.ataque_base IS NOT NULL
            AND d.defesa_base IS NOT NULL AND d.ataque_especial_base IS NOT NULL
            AND d.defesa_especial_base IS NOT NULL AND d.velocidade_base IS NOT NULL AND d.especial_base IS NULL THEN 1 ELSE 0 END) AS seis_estatisticas_com_fonte,
        SUM(CASE WHEN d.fonte_estatisticas IS NOT NULL AND d.hp_base IS NOT NULL AND d.ataque_base IS NOT NULL
            AND d.defesa_base IS NOT NULL AND d.velocidade_base IS NOT NULL AND d.especial_base IS NOT NULL
            AND d.ataque_especial_base IS NULL AND d.defesa_especial_base IS NULL AND j.geracao=1
            THEN 1 ELSE 0 END) AS cinco_estatisticas_especial_unico_com_fonte,
        SUM(CASE WHEN d.especial_base IS NOT NULL AND (d.ataque_especial_base IS NOT NULL OR d.defesa_especial_base IS NOT NULL)
            THEN 1 ELSE 0 END) AS fichas_com_sistemas_estatisticos_misturados,
        SUM(CASE WHEN d.id_dados_forma IS NOT NULL AND d.fonte_tipos IS NULL THEN 1 ELSE 0 END) AS tipos_sem_fonte,
        SUM(CASE WHEN d.id_dados_forma IS NOT NULL AND d.fonte_estatisticas IS NULL THEN 1 ELSE 0 END) AS estatisticas_sem_fonte,
        SUM(CASE WHEN EXISTS (SELECT 1 FROM HABILIDADE_FORMA_JOGO h
            WHERE h.id_dados_forma=d.id_dados_forma AND h.fonte_url IS NOT NULL) THEN 1 ELSE 0 END) AS fichas_com_alguma_habilidade_com_fonte,
        SUM(CASE WHEN EXISTS (SELECT 1 FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mf.id_dados_forma=d.id_dados_forma AND mo.nome='Encontro selvagem') THEN 1 ELSE 0 END) AS fichas_metodo_selvagem,
        SUM(CASE WHEN EXISTS (SELECT 1 FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mf.id_dados_forma=d.id_dados_forma AND mo.nome='Presente no jogo') THEN 1 ELSE 0 END) AS fichas_metodo_presente,
        SUM(CASE WHEN EXISTS (SELECT 1 FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mf.id_dados_forma=d.id_dados_forma AND mo.nome='Ovo recebido no jogo') THEN 1 ELSE 0 END) AS fichas_metodo_ovo,
        SUM(CASE WHEN EXISTS (SELECT 1 FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mf.id_dados_forma=d.id_dados_forma AND mo.nome='Incursão Teracristal de evento') THEN 1 ELSE 0 END) AS fichas_metodo_evento_sv,
        (SELECT COUNT(*) FROM MECANICA_JOGO m WHERE m.id_jogo=j.id_jogo) AS mecanicas,
        (SELECT COUNT(*) FROM MECANICA_JOGO m WHERE m.id_jogo=j.id_jogo AND m.versao='regras-parciais-documentadas') AS mecanicas_parciais,
        (SELECT COUNT(*) FROM MECANICA_JOGO m WHERE m.id_jogo=j.id_jogo AND NOT EXISTS
            (SELECT 1 FROM MECANICA_SISTEMA_ATRIBUTO s WHERE s.id_mecanica=m.id_mecanica)) AS mecanicas_sem_sistemas_registrados
        FROM JOGO j LEFT JOIN DADOS_FORMA_JOGO d USING(id_jogo)
        GROUP BY j.id_jogo ORDER BY j.geracao,j.nome""")]
    return {'snapshot_commit': manifest['commit'], 'fonte_url': manifest['source_url'], 'contagens_banco': counts,
        'cobertura_snapshot': {'especies_importadas': matched['especies'], 'especies_fonte': len(data['pokemon_species.csv']),
                              'formas_importadas': matched['formas'], 'formas_fonte': len(data['pokemon_forms.csv']),
                              'versoes_fonte': len(data['versions.csv']), 'versoes_identificadas': len(
                                  {r['identifier'].casefold() for r in data['versions.csv']} &
                                  {r[0].casefold() for r in db.execute('SELECT codigo_versao_pokeapi FROM JOGO WHERE codigo_versao_pokeapi IS NOT NULL')})},
        'nomes_exibidos': 'Inglês da fonte, sem tradução portuguesa confirmada; códigos de forma preservados.',
        'pendencias': ['Fichas e presença por jogo', 'Tipos, habilidades e atributos históricos para contextos ainda não importados',
                      'Mecânicas e limites para versões ainda não contempladas', 'Outros regulamentos, formas e elegibilidades com fontes específicas',
                      'Outros perfis de referência competitiva verificados'],
        'fichas_outras_fontes_preservadas': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url IS NULL OR fonte_url NOT IN (?,?,?,?)", (manifest['files']['encounters.csv.gz']['url'],DRAGAPULT_SOURCE,SV_STARTER_SOURCE,SV_RAID_SOURCE)).fetchone()[0],
        'fichas_dragapult_guia_vgc': db.execute('SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url=?',(DRAGAPULT_SOURCE,)).fetchone()[0],
        'fichas_iniciais_scarlet_violet': db.execute('SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url=?',(SV_STARTER_SOURCE,)).fetchone()[0],
        'fichas_evento_sv_2024': db.execute('SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url=?',(SV_RAID_SOURCE,)).fetchone()[0],
        'perfis_referencia_guia_vgc': db.execute("SELECT count(*) FROM PERFIL_ANALISE WHERE tipo_perfil='referencia_competitiva' AND fonte_url=?",(DRAGAPULT_SOURCE,)).fetchone()[0],
        'jogos_legados_identidade_ambigua': db.execute("SELECT count(*) FROM JOGO WHERE codigo_versao_pokeapi IS NULL AND nome COLLATE NOCASE IN ('Red','Blue')").fetchone()[0],
        'fichas_tipos_com_fonte': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_tipos IS NOT NULL").fetchone()[0],
        'fichas_estatisticas_com_fonte': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_estatisticas IS NOT NULL").fetchone()[0],
        'fichas_especial_unico_com_fonte': db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO d JOIN JOGO j USING(id_jogo)
            WHERE d.fonte_estatisticas IS NOT NULL AND d.hp_base IS NOT NULL AND d.ataque_base IS NOT NULL
            AND d.defesa_base IS NOT NULL AND d.velocidade_base IS NOT NULL AND d.especial_base IS NOT NULL
            AND d.ataque_especial_base IS NULL AND d.defesa_especial_base IS NULL AND j.geracao=1""").fetchone()[0],
        'fichas_com_sistemas_estatisticos_misturados': db.execute("""SELECT count(*) FROM DADOS_FORMA_JOGO
            WHERE especial_base IS NOT NULL AND (ataque_especial_base IS NOT NULL OR defesa_especial_base IS NOT NULL)""").fetchone()[0],
        'mecanicas_sem_sistemas_registrados': db.execute("SELECT count(*) FROM MECANICA_JOGO m WHERE NOT EXISTS (SELECT 1 FROM MECANICA_SISTEMA_ATRIBUTO s WHERE s.id_mecanica=m.id_mecanica)").fetchone()[0],
        'mecanicas_parciais_identificadas': db.execute("SELECT count(*) FROM MECANICA_JOGO WHERE versao='regras-parciais-documentadas'").fetchone()[0],
        'habilidades_com_fonte': db.execute("SELECT count(*) FROM HABILIDADE_FORMA_JOGO").fetchone()[0],
        'cobertura_por_jogo': games,
        'interpretacao_cobertura': {
            'sem_fonte': 'Não verificado; ausência de ficha ou vínculo não comprova ausência no jogo.',
            'seis_estatisticas': 'Fonte e seis valores modernos preenchidos; a primeira geração usa cinco estatísticas, com Especial único.',
            'especial_unico': 'Fonte e cinco valores preenchidos com Especial único; não se aplica aos dois campos especiais modernos.',
            'habilidades': 'Contagem de fichas com pelo menos um vínculo; não comprova obtenção por evento ou método.',
            'nao_aplicavel': 'Habilidades não se aplicam às gerações I e II nem a Pokémon: Let’s Go; consulte a fonte na ficha.'},
        'fichas_encontro_documentado': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url=?", (manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'fichas_metodo_selvagem': db.execute("""SELECT count(DISTINCT mf.id_dados_forma) FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mo.nome='Encontro selvagem' AND mf.fonte_url=?""",(manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'fichas_metodo_presente': db.execute("""SELECT count(DISTINCT mf.id_dados_forma) FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mo.nome='Presente no jogo' AND mf.fonte_url=?""",(manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'fichas_metodo_ovo': db.execute("""SELECT count(DISTINCT mf.id_dados_forma) FROM METODO_FORMA_JOGO mf JOIN METODO_OBTENCAO mo USING(id_metodo)
            WHERE mo.nome='Ovo recebido no jogo' AND mf.fonte_url=?""",(manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'observacao': 'Cobertura é relativa ao snapshot, não certifica completude oficial atual. Ausência de ficha não indica ausência no jogo.'}
