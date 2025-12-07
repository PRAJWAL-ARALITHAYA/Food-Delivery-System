import os, time, sys
from pathlib import Path

root = Path('.').resolve()
ignore_dirs = {'node_modules','.git','backend/venv','frontend/node_modules'}

def walk_files():
    files = {}
    for p in root.rglob('*'):
        try:
            if any(part in ignore_dirs for part in p.parts):
                continue
            if p.is_file():
                files[str(p)] = p.stat().st_mtime
        except Exception:
            pass
    return files

print('Monitoring file changes in', root)
initial = walk_files()
start = time.time()
duration = 20
last = initial
while time.time() - start < duration:
    time.sleep(1)
    current = walk_files()
    changed = []
    for f,m in current.items():
        if f not in last:
            changed.append((f,'CREATED'))
        elif last[f] != m:
            changed.append((f,'MODIFIED'))
    for f in list(last.keys()):
        if f not in current:
            changed.append((f,'DELETED'))
    if changed:
        print(time.strftime('%H:%M:%S'), 'Changes detected:')
        for f,s in changed:
            print(' ', s, f)
        print('---')
    last = current

print('Monitoring finished')
sys.exit(0)
