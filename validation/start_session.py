"""Launch a fresh local study workspace; never reuse or erase an existing DB."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('participant', choices=[f'P{i:02}' for i in range(1, 9)])
parser.add_argument('case', choices=['practice', 'new', 'duplicate', 'conflict', 'unresolved'])
parser.add_argument('--port', type=int, default=8769)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
db = root / '.runtime/validation/study' / args.participant / f'{args.case}.db'
if db.exists():
    parser.error(f'Workspace already exists: {db}. Preserve it; do not overwrite a study attempt.')
db.parent.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, NESTPROOF_DB=str(db))
print(f'Fresh {args.participant}/{args.case}: http://127.0.0.1:{args.port}', flush=True)
subprocess.run([sys.executable, '-m', 'uvicorn', 'nestproof.app:app', '--host', '127.0.0.1', '--port', str(args.port)], cwd=root, env=env, check=True)
