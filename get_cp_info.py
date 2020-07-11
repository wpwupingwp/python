#!/usr/bin/python3

from pathlib import Path
from subprocess import run
from sys import argv
from Bio import SeqIO


at_ratio = []
workdir = Path(argv[1]).absolute()
subs = workdir.glob('*')
for sub in subs:
    for file_ in sub.glob('*'):
        # temporary use rosa
        # run(f'python -m novowrap.validate -taxon {sub.stem} -input {file_} '
        run(f'python -m novowrap.validate -taxon Rosa -input {file_} '
            f'-out {sub/file_.stem}', shell=True)
        s = SeqIO.read(file_, 'fasta')
        s_seq = s.seq.upper()
        # ignore ambiguous base
        at = (s.seq.count('A')+s.seq.count('T')) / len(s_seq)
        at_ratio.append([sub.stem, file_.stem, str(at)])
with open(workdir/'AT.csv', 'w') as out:
    for line in at_ratio:
        out.write(','.join(line)+'\n')
