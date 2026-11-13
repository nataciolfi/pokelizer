"""Generate the Stage 1 dictionary and every FK cardinality from executable SQL.

Run from any directory; --check compares generated documentation without writing.
Conditional minima and domain rules are deliberately described separately.
"""
import argparse
from collections import defaultdict
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def render():
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / 'backend/schema.sql').read_text())
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    out = ['# Dicionário lógico/físico e relacionamentos', '',
           'Gerado de `backend/schema.sql` por `python tools/document_model.py`. Não editar manualmente. Os desenhos brModelo são a representação visual complementar. O SQL e seus gatilhos definem restrições não expressáveis apenas pelas linhas do desenho.', '',
           '## Convenções e cardinalidades condicionais', '',
           'Cada linha da matriz é uma relação por FK, inclusive papéis diferentes entre as mesmas tabelas. Filho→pai indica quantos pais um filho referencia; pai→filho indica quantos filhos um pai pode ter. Mínimo zero no pai é permitido sem presumir que o catálogo/usuário esteja populado. Toda FK tem atualização RESTRICT; IDs são imutáveis. N significa muitos.', '',
           '- ESPECIE rascunho pode ter 0..N formas; ESPECIE completa exige 1..N formas e exatamente uma padrão. A unicidade parcial e os gatilhos também protegem atualização/exclusão.',
           '- DADOS_FORMA_JOGO pode ter 0..2 tipos no estado não verificado; quando status_tipos=aplicavel exige 1..2, incluindo posição primária; nao_aplicavel exige zero.',
           '- PERFIL_ANALISE personalizado exige exatamente um USUARIO; referência exige zero usuários e evidência. REGULAMENTO é opcional no perfil.',
           '- Origem de exemplar é opcional; quando id_dados_forma_origem é informado, id_jogo_origem é obrigatório e deve corresponder ao jogo daquela ficha.',
           '- MECANICA_JOGO é opcional no exemplar sem valores contextuais conhecidos. Natureza, habilidade, nível e valores numéricos exigem mecânica confirmada compatível.',
           '- Uma espécie/forma/jogo pode existir sem ficha, coleção, perfil, regulamento ou transformação. Não há participação mínima presumida nesses filhos.', '',
           '## Matriz completa de relações', '',
           '| Filho e papel (campos) | Pai (campos) | Filho→pai | Pai→filho | Unicidade da relação | Exclusão do pai |',
           '|---|---|---|---|---|---|']
    details = []
    count = 0
    for table in tables:
        cols = [dict(r) for r in db.execute(f'PRAGMA table_info("{table}")')]
        byname = {c['name']: c for c in cols}
        unique = []
        pk = tuple(c['name'] for c in sorted(cols, key=lambda x: x['pk']) if c['pk'])
        if pk: unique.append(pk)
        unique_display = [('PK', pk)] if pk else []
        for idx in db.execute(f'PRAGMA index_list("{table}")'):
            if idx['unique']:
                fs = tuple(r['name'] for r in db.execute(f'PRAGMA index_info("{idx["name"]}")'))
                if not idx['partial']: unique.append(fs)
                if idx['origin'] != 'pk': unique_display.append(('UNIQUE parcial' if idx['partial'] else 'UNIQUE', fs))
        fks = defaultdict(list)
        for fk in db.execute(f'PRAGMA foreign_key_list("{table}")'): fks[fk['id']].append(dict(fk))
        fkfields = {f['from'] for group in fks.values() for f in group}
        for key, group in sorted(fks.items()):
            group.sort(key=lambda x: x['seq'])
            fs = tuple(f['from'] for f in group)
            target = tuple(f['to'] for f in group)
            optional = any(not byname[c]['notnull'] and not byname[c]['pk'] for c in fs)
            reverse_one = any(set(u).issubset(fs) for u in unique)
            note = 'Campos podem repetir; combinação limitada pelas chaves da tabela'
            if reverse_one: note = 'Campos FK são únicos no filho'
            out.append(f"| {table} ({', '.join(fs)}) | {group[0]['table']} ({', '.join(target)}) | {'0..1' if optional else '1..1'} | {'0..1' if reverse_one else '0..N'} | {note} | {group[0]['on_delete']} |")
            count += 1
        details += ['', f'## {table}', '',
                    '| Campo | Tipo SQLite | Nulo permitido | Chave | Default |',
                    '|---|---|---|---|---|']
        for c in cols:
            flags = (['PK'] if c['pk'] else []) + (['FK'] if c['name'] in fkfields else [])
            details.append(f"| {c['name']} | {c['type']} | {'não' if c['notnull'] or c['pk'] else 'sim'} | {', '.join(flags) or '—'} | {c['dflt_value'] if c['dflt_value'] is not None else '—'} |")
        details += ['', 'Chaves: ' + '; '.join(f"{kind}({', '.join(fs)})" for kind, fs in unique_display) + '.', '',
                    'CHECKs, índices e gatilhos: consultar a definição desta tabela em [schema.sql](../../backend/schema.sql) e a [matriz de invariantes](integrity.md).']
    db.close()
    out += ['', f'Contagem: **{len(tables)} tabelas de domínio**, **{count} relações FK**. SCHEMA_MIGRATION é metadado operacional criado pelo executor Python, fora do modelo de domínio.']
    return '\n'.join(out + details) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'docs/stage1/data-model.md'
    content = render()
    if args.check:
        if not path.is_file() or path.read_text() != content:
            raise SystemExit('Modelo textual desatualizado; execute python tools/document_model.py')
        print('Dicionário e cardinalidades conferem com o SQL.')
    else:
        path.write_text(content)
        print(path)
