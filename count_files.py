from sys import argv
from pathlib import Path

files = Path(argv[1]).glob('*')
n_dir = 0
n_file = 0
n_other = 0

for f in files:
    if f.is_dir():
        n_dir += 1
    elif f.is_file():
        n_file += 1
    else:
        n_other += 1
print(n_dir, 'folders')
print(n_file, 'files')
print(n_other, 'other objects')
print(n_dir+n_file+n_other, 'in all.')
