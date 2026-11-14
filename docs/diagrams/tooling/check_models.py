"""Check the actual brModelo XML exports, native/export hashes and current SQL metadata."""
from pathlib import Path
import ast, collections, hashlib, json, xml.etree.ElementTree as ET
from export_models import ROOT, OUT, SCHEMA, metadata, relationship_name

def val(node, name):
    item=node.find(name)
    assert item is not None, (node.tag,name)
    return item.get('Valor')

def verify():
    manifest=json.loads((OUT/'manifest.json').read_text())
    assert manifest['schema_sha256']==hashlib.sha256(SCHEMA.read_bytes()).hexdigest(), 'schema changed; regenerate diagrams'
    assert manifest['native_wrapper_metadata']['autor']=='Pokelizer project' and manifest['native_wrapper_metadata']['data']==''
    tables,fks=metadata()
    assert manifest['tables']==tables and manifest['relationships']==fks
    for name,digest in manifest['artifacts'].items():
        assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest, name+' changed after export'
        if name.endswith('.brM3'):
            native=(OUT/name).read_bytes()
            assert native[:4]==b'\xac\xed\x00\x05', 'not a native Java serialized brModelo model'
            assert b'Pokelizer project' in native and b'Carlos Henrique' not in native and b'13-02-2012' not in native, 'unexpected native author/date metadata'
    logical=ET.parse(OUT/'logico.xml').getroot()
    conceptual=ET.parse(OUT/'conceitual.xml').getroot()
    lt={t.findtext('Texto'):t for t in logical.findall('Tabela')}
    ct={t.findtext('Texto'):t for t in conceptual.findall('Entidade')}
    assert set(lt)==set(ct)==set(tables)
    cids={v.get('ID'):k for k,v in ct.items()}
    attributes={a.get('ID'):a for a in conceptual.findall('Atributo')}
    attached=collections.defaultdict(list)
    for link in conceptual.findall('Ligacao'):
        ends=link.find('Ligacoes').attrib
        for x,y in ((ends['PontaA'],ends['PontaB']),(ends['PontaB'],ends['PontaA'])):
            if x in attributes and y in cids:attached[cids[y]].append(attributes[x])
    for name,spec in tables.items():
        cols=lt[name].findall('Campos/Campo')
        assert [c.findtext('Texto') for c in cols]==[c['name'] for c in spec['fields']], name
        assert len(attached[name])==len(spec['fields']), name
        ca={a.findtext('Texto'):a for a in attached[name]}
        fkcolumns={n for f in fks if f['child']==name for n in f['columns']}
        for xml,col in zip(cols,spec['fields']):
            assert xml.findtext('Tipo')==col['type'], (name,col['name'],'type')
            assert (xml.findtext('Complemento') or '')==('NOT NULL' if col['notnull'] or col['pk'] else ''), (name,col['name'],'nullability')
            assert (val(xml,'Key')=='true')==bool(col['pk']), (name,col['name'],'PK')
            assert (val(xml,'Fkey')=='true')==(col['name'] in fkcolumns), (name,col['name'],'FK')
            assert (val(ca[col['name']],'Identificador')=='true')==bool(col['pk']), (name,col['name'],'conceptual identifier')
            assert (val(ca[col['name']],'Opcional')=='true')==(not bool(col['notnull'] or col['pk'])), (name,col['name'],'conceptual optionality')
        uniques=[]
        for constraint in lt[name].findall('Constraints/Constraint'):
            if val(constraint,'Tipo')=='1':
                indexes=ast.literal_eval(constraint.find('ConstraintOrigem').get('CamposOrigem'))
                uniques.append([cols[i].findtext('Texto') for i in indexes])
        assert uniques==spec['unique'], (name,'unique keys')
    lids={t.get('ID'):name for name,t in lt.items()}
    lines={l.get('ID'):l for l in logical.findall('LogicoLinha')}
    crels={r.get('ID'):r for r in conceptual.findall('Relacionamento')}
    for i,f in enumerate(fks,1):
        child=lt[f['child']];fk=next(c for c in child.findall('Constraints/Constraint') if val(c,'Nome')=='FK_'+str(i))
        origin=fk.find('ConstraintOrigem');parentid,index=origin.get('ID').split(',')
        assert lids[parentid]==f['parent']
        src=ast.literal_eval(origin.get('CamposOrigem'));dst=ast.literal_eval(origin.get('CamposDestino'))
        parent=lt[f['parent']]
        assert [parent.findall('Campos/Campo')[n].findtext('Texto') for n in src]==f['targets']
        assert [child.findall('Campos/Campo')[n].findtext('Texto') for n in dst]==f['columns']
        assert fk.findtext('DdlOnDelete')==f['delete'] and fk.findtext('DdlOnUpdate')==f['update']
        line=lines[fk.find('LigacaoParaOrigem').get('ID')]
        assert lids[line.find('Ligacoes').get('PontaA')]==f['parent'] and lids[line.find('Ligacoes').get('PontaB')]==f['child']
        cards=line.findall('LogicoCardinalidade')
        assert val(cards[0],'Card')==('0' if f['required'] else '1') and val(cards[1],'Card')=='3'
        rel=next(r for r in crels.values() if r.findtext('Texto')=='R'+str(i)+' '+relationship_name(f))
        ends=[]
        for link in conceptual.findall('Ligacao'):
            e=link.find('Ligacoes')
            if rel.get('ID') in e.attrib.values():
                other=e.get('PontaB') if e.get('PontaA')==rel.get('ID') else e.get('PontaA')
                ends.append((cids[other],val(link.find('Cardinalidade'),'Card')))
        assert sorted(ends)==sorted([(f['child'],'0' if f['required'] else '1'),(f['parent'],'3')])
    assert len(lines)==len(crels)==len(fks)
    for prefix in ('conceitual','logico'):
        pages=sorted(OUT.glob(prefix+'-relacoes-*.xml'))
        count=sum(len(ET.parse(p).getroot().findall('Relacionamento' if prefix=='conceitual' else 'LogicoLinha')) for p in pages)
        assert count==len(fks), (prefix,'enlarged sheets missing a relationship')
    print(f'brModelo consistent: {len(tables)} entities, {sum(len(t["fields"]) for t in tables.values())} fields, {len(fks)} relationships; all native/export hashes intact.')

if __name__=='__main__':verify()
