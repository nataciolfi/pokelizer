"""Pinned upstream identities. Game mechanics are never inferred from global rows."""
import csv
import hashlib
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
        if name.endswith('.csv'):
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
            existing = db.execute('SELECT * FROM FORMA WHERE id_especie=? AND codigo_forma=?', (species, code)).fetchone()
            if existing and (existing['fonte_url'] != source or existing['forma_padrao'] != default):
                raise ValueError(f'Conflito em forma {code}; importação revertida.')
            if not existing:
                db.execute('INSERT INTO FORMA(id_especie,codigo_forma,nome_forma,forma_padrao,estado_forma,fonte_url,data_verificacao) VALUES(?,?,?,?,?,?,?)',
                    (species, code, code, default, 'temporario' if r['is_battle_only']=='1' else 'nao_verificado', source, date))
        for r in data['versions.csv']:
            name = game_names.get(r['id'], r['identifier'])
            existing = db.execute('SELECT * FROM JOGO WHERE nome=? COLLATE NOCASE', (name,)).fetchone()
            if existing and existing['fonte_url'] != source:
                raise ValueError(f'Conflito em jogo {name}; catálogo existente preservado.')
            if not existing:
                db.execute('INSERT INTO JOGO(nome,geracao,fonte_url,data_verificacao) VALUES(?,?,?,?)',
                    (name, int(groups[r['version_group_id']]['generation_id']), source, date))
        if db.execute('PRAGMA foreign_key_check').fetchone():
            raise ValueError('Snapshot violou integridade; carga revertida.')
    return cobertura(directory)


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
                      'Versões de mecânica e limites documentados', 'Regulamentos e elegibilidade com fontes específicas',
                      'Perfis de referência competitiva verificados'],
        'observacao': 'Cobertura é relativa ao snapshot, não certifica completude oficial atual. Ausência de ficha não indica ausência no jogo.'}
