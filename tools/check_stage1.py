"""Run the repeatable delivery checks from a clone with requirements installed."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT / 'backend') + os.pathsep + env.get('PYTHONPATH', '')
commands = [
    ['backend/tools/build_schema.py', '--check'],
    ['tools/document_model.py', '--check'],
    ['docs/diagrams/tooling/check_models.py'],
    ['docs/uml/check_uml.py'],
    ['tools/check_links.py'],
    ['-m', 'pytest', 'backend/tests', '-q'],
]
for args in commands:
    print('RUN:', sys.executable, *args, flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)
print('All repeatable Stage 1 checks passed. Visual inspection is documented separately.')
