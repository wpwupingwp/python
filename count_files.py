from sys import argv
from pathlib import Path

files = Path(argv[1]).glob('*')
print(len(list(files))
