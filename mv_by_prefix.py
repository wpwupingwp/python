#!/usr/bin/python3

from pathlib import Path
from shutil import move
from sys import argv
from timeit import default_timer as timer


start = timer()
print("python3 mv_by_prefix.py folder")
folder = Path(argv[1])
files = folder.glob("*")
accept_type = (
    "gene",
    "CDS",
    "tRNA",
    "rRNA",
    "misc_feature",
    "misc_RNA",
    "spacer",
    "mosaic_spacer",
    "intron",
)
folder_dict = {}
for f in accept_type:
    p = folder / f
    p.mkdir()
    folder_dict[f] = p
for fasta in files:
    if fasta.is_dir():
        continue
    prefix = fasta.name.split(".")[0]
    dest = folder_dict[prefix] / fasta.name
    move(fasta, dest)
end = timer()
print(end - start, "seconds")
