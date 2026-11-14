"""Run all inherited artifact/integrity checks, API regressions and professor demo."""
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
env=os.environ.copy()
env['PYTHONPATH']=str(ROOT/'backend')+os.pathsep+env.get('PYTHONPATH','')
for args in [['tools/check_stage1.py'],['tools/demonstrate_stage2.py']]:
    subprocess.run([sys.executable,*args],cwd=ROOT,env=env,check=True)
print('Stage 2 repeatable checks passed. Consult visual-review.md and coverage.json for their separate scope.')
