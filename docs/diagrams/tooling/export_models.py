"""Feed physical metadata to the genuine brModelo object model; never draw images here."""
from pathlib import Path
import hashlib, json, sqlite3, subprocess, os, tempfile
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/diagrams'
SCHEMA=ROOT/'backend/schema.sql'

def metadata():
    db=sqlite3.connect(':memory:');db.executescript(SCHEMA.read_text())
    tables={}
    fks=[]
    for name, in db.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY rowid"):
        fields=[dict(zip(('cid','name','type','notnull','default','pk'),r)) for r in db.execute(f'PRAGMA table_info("{name}")')]
        unique=[]
        for idx in db.execute(f'PRAGMA index_list("{name}")'):
            if idx[2]:
                cols=[r[2] for r in db.execute(f'PRAGMA index_info("{idx[1]}")')]
                # Partial uniqueness is documented by the physical schema, not unconditional here.
                if not idx[4]: unique.append(cols)
        tables[name]={'fields':fields,'unique':unique}
        grouped={}
        for r in db.execute(f'PRAGMA foreign_key_list("{name}")'):
            grouped.setdefault(r[0],[]).append(r)
        for group in grouped.values():
            group.sort(key=lambda r:r[1]);cols=[r[3] for r in group]
            required=all(next(c for c in fields if c['name']==n)['notnull'] or next(c for c in fields if c['name']==n)['pk'] for n in cols)
            fks.append({'child':name,'parent':group[0][2],'columns':cols,'targets':[r[4] for r in group], 'required':bool(required),'delete':group[0][6],'update':group[0][5]})
    return tables,fks

def main():
    tables,fks=metadata();OUT.mkdir(exist_ok=True)
    data=OUT/'tooling/model-input.tsv'
    with data.open('w') as f:
        for name, table in tables.items():
            f.write('T\t'+name+'\n')
            fkcols={n for k in fks if k['child']==name for n in k['columns']}
            for col in table['fields']:
                f.write('\t'.join(map(str,('C',name,col['name'],col['type'],col['notnull'],col['pk'],int(col['name'] in fkcols))))+'\n')
            for i,cols in enumerate(table['unique']): f.write('\t'.join(('U',name,str(i),','.join(cols)))+'\n')
        for i,fk in enumerate(fks,1):
            f.write('\t'.join(map(str,('F',i,fk['child'],fk['parent'],','.join(fk['columns']),','.join(fk['targets']),int(fk['required']),fk['delete'],fk['update'])))+'\n')
    jar=Path(os.environ['BRMODELO_JAR']).resolve()
    javac=os.environ.get('JAVAC','javac');java=os.environ.get('JAVA','java')
    source=OUT/'tooling/ExportModels.java'
    with tempfile.TemporaryDirectory(prefix='pokelizer-brmodelo-') as build:
        subprocess.run([javac,'-cp',str(jar),'-d',build,str(source)],check=True)
        result=subprocess.run([java,'-Djava.awt.headless=true','-XX:-UsePerfData','-Xmx1500m','-cp',str(jar)+os.pathsep+build,'ExportModels',str(data),str(OUT)],cwd=build,check=True,capture_output=True,text=True)
    (OUT/'tooling/reopen-verification.txt').write_text(result.stdout)
    manifest={'native_wrapper_metadata':{'autor':'Pokelizer project','data':'','method':'Public GuardaPadraoBrM fields; native diagram payload preserved'},'schema_sha256':hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),'brmodelo_version':'3.3.2 (official distribution 3.32)','brmodelo_url':'https://brmodelo.com/brModelo.jar','brmodelo_jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'tables':tables,'relationships':fks,'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*')) if p.suffix in ('.brM3','.xml','.png')}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(result.stdout)
if __name__=='__main__':main()
