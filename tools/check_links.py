"""Check local Markdown delivery links; historical snapshots remain non-normative."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
count = 0
for path in [ROOT / 'README.md', ROOT / 'backend/README.md', *sorted((ROOT / 'docs').rglob('*.md'))]:
    if 'archive' in path.relative_to(ROOT).parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = target.strip().split(' "', 1)[0].strip('<>')
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            continue
        count += 1
        resolved = path.parent / unquote(url.path)
        if not resolved.exists():
            errors.append(f'{path.relative_to(ROOT)}: {target}')
if errors:
    raise SystemExit('Broken delivery links:\n' + '\n'.join(errors))
print(f'{count} local delivery links resolve (historical archives excluded).')
