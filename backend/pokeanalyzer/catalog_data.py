"""Pinned upstream identities. Game mechanics are never inferred from global rows."""
import csv
import hashlib
import gzip
from collections import Counter
import json
from pathlib import Path
from .db import get_db, transaction

SNAPSHOT = Path(__file__).resolve().parents[1] / 'data' / 'pokeapi'


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
            existing = db.execute('SELECT * FROM JOGO WHERE nome=? COLLATE NOCASE', (name,)).fetchone()
            if existing and existing['fonte_url'] != source:
                raise ValueError(f'Conflito em jogo {name}; catálogo existente preservado.')
            if not existing:
                db.execute('INSERT INTO JOGO(nome,geracao,fonte_url,data_verificacao) VALUES(?,?,?,?)',
                    (name, int(groups[r['version_group_id']]['generation_id']), source, date))
        importar_encontros(db, data, manifest)
        from .curated_data import importar_mecanicas_swsh
        importar_mecanicas_swsh(db, data)
        from .contextual_data import importar_contextos_swsh
        importar_contextos_swsh(db, data, manifest)
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
    names = {r['version_id']: r['name'] for r in data['version_names.csv'] if r['local_language_id'] == '9'}
    versions = {v['id']: names.get(v['id'], v['identifier']) for v in data['versions.csv']}
    name_counts = Counter(name.casefold() for name in versions.values())
    versions = {vid: name for vid, name in versions.items() if name_counts[name.casefold()] == 1}
    source = manifest['files']['encounters.csv.gz']['url']
    date = manifest['files']['encounters.csv.gz']['retrieved_at']
    # Explicit wild methods only: gifts, NPC trades, bonus discs and snag events
    # also occur in encounters.csv and must not be described as wild capture.
    wild_method_ids = {str(n) for n in (*range(1,18), 22, 23, 24)}
    wild_slots = {r['id']: r['version_group_id'] for r in data['encounter_slots.csv'] if r['encounter_method_id'] in wild_method_ids}
    version_groups = {r['id']: r['version_group_id'] for r in data['versions.csv']}
    # Absence of a matching encounter never implies absence in the game.
    pairs = sorted({(r['pokemon_id'], r['version_id']) for r in data['encounters.csv']
                    if r['pokemon_id'] in one_form and r['version_id'] in versions and r['encounter_slot_id'] in wild_slots and wild_slots[r['encounter_slot_id']] == version_groups[r['version_id']]},
                   key=lambda p: (int(p[1]), int(p[0])))
    method = db.execute("SELECT id_metodo FROM METODO_OBTENCAO WHERE nome=? COLLATE NOCASE", ('Encontro selvagem',)).fetchone()
    if not method:
        db.execute("INSERT INTO METODO_OBTENCAO(nome,descricao) VALUES(?,?)", ('Encontro selvagem','Encontro selvagem documentado na fonte; condições variam por local.'))
        method = db.execute("SELECT last_insert_rowid()").fetchone()
    for pid, vid in pairs:
        row = one_form[pid]
        existing_form = db.execute("SELECT f.id_forma FROM FORMA f JOIN ESPECIE e USING(id_especie) WHERE e.numero_nacional=? AND f.codigo_forma=?", (int(pokemon[pid]['species_id']), row['identifier'])).fetchone()
        game = db.execute("SELECT id_jogo FROM JOGO WHERE nome=? COLLATE NOCASE", (versions[vid],)).fetchone()
        if not existing_form or not game:
            raise ValueError('Forma ou jogo da fonte não encontrado; carga revertida.')
        current = db.execute("SELECT * FROM DADOS_FORMA_JOGO WHERE id_forma=? AND id_jogo=?", (existing_form[0],game[0])).fetchone()
        if current:
            # Curated or conflicting facts are never replaced. They remain visible in the coverage report.
            continue
        cursor = db.execute("""INSERT INTO DADOS_FORMA_JOGO(id_forma,id_jogo,status_presenca,pode_ser_registrada,fonte_url,data_verificacao)
                                VALUES(?,?,'nativa','sim',?,?)""", (existing_form[0],game[0],source,date))
        db.execute("INSERT INTO METODO_FORMA_JOGO(id_dados_forma,id_metodo,fonte_url,data_verificacao) VALUES(?,?,?,?)",
                   (cursor.lastrowid,method[0],source,date))

def cobertura(directory=SNAPSHOT):
    manifest, data = ler_snapshot(directory)
    db = get_db()
    counts = {t: db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in
        ('ESPECIE','FORMA','JOGO','DADOS_FORMA_JOGO','MECANICA_JOGO','REGULAMENTO','ELEGIBILIDADE_FORMA_REGULAMENTO')}
    matched = {
        'especies': db.execute('SELECT count(*) FROM ESPECIE WHERE fonte_url=?', (manifest['source_url'],)).fetchone()[0],
        'formas': db.execute('SELECT count(*) FROM FORMA WHERE fonte_url=?', (manifest['source_url'],)).fetchone()[0]}
    return {'snapshot_commit': manifest['commit'], 'fonte_url': manifest['source_url'], 'contagens_banco': counts,
        'cobertura_snapshot': {'especies_importadas': matched['especies'], 'especies_fonte': len(data['pokemon_species.csv']),
                              'formas_importadas': matched['formas'], 'formas_fonte': len(data['pokemon_forms.csv'])},
        'nomes_exibidos': 'Inglês da fonte, sem tradução portuguesa confirmada; códigos de forma preservados.',
        'pendencias': ['Fichas e presença por jogo', 'Tipos, habilidades e atributos históricos por jogo',
                      'Mecânicas e limites fora de Sword/Shield', 'Regulamentos e elegibilidade com fontes específicas',
                      'Perfis de referência competitiva verificados'],
        'fichas_outras_fontes_preservadas': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url IS NULL OR fonte_url!=?", (manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'versoes_excluidas_identidade_ambigua': ['red', 'red-japan', 'blue', 'blue-japan'],
        'fichas_tipos_com_fonte': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_tipos IS NOT NULL").fetchone()[0],
        'fichas_estatisticas_com_fonte': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_estatisticas IS NOT NULL").fetchone()[0],
        'habilidades_com_fonte': db.execute("SELECT count(*) FROM HABILIDADE_FORMA_JOGO").fetchone()[0],
        'fichas_encontro_documentado': db.execute("SELECT count(*) FROM DADOS_FORMA_JOGO WHERE fonte_url=?", (manifest['files']['encounters.csv.gz']['url'],)).fetchone()[0],
        'observacao': 'Cobertura é relativa ao snapshot, não certifica completude oficial atual. Ausência de ficha não indica ausência no jogo.'}
