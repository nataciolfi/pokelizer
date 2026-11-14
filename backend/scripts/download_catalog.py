"""Re-download the exact reviewed upstream bytes to a NEW directory, never update the lock."""
from pathlib import Path
import argparse
import hashlib
import json
import gzip
import io
import urllib.request

parser=argparse.ArgumentParser()
parser.add_argument('destination',type=Path)
args=parser.parse_args()
manifest_path=Path(__file__).resolve().parents[1]/'data/pokeapi/manifest.json'
manifest=json.loads(manifest_path.read_text())
args.destination.mkdir(exist_ok=False,parents=True)
for name,meta in manifest['files'].items():
    with urllib.request.urlopen(meta['url'],timeout=60) as response:
        raw=response.read()
    if meta.get('compression') == 'gzip':
        if hashlib.sha256(raw).hexdigest() != meta['raw_sha256']:
            raise SystemExit(f'Hash divergente em {name}; não importar.')
        buffer = io.BytesIO()
        with gzip.GzipFile(filename='', mode='wb', fileobj=buffer, mtime=0) as compressed:
            compressed.write(raw)
        raw = buffer.getvalue()
    if hashlib.sha256(raw).hexdigest()!=meta['sha256']:
        raise SystemExit(f'Hash divergente em {name}; não importar. Origem/destino anterior intactos.')
    (args.destination/name).write_bytes(raw)
(args.destination/'manifest.json').write_bytes(manifest_path.read_bytes())
print(args.destination)
