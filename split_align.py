#!/usr/bin/python3

from sys import argv
from Bio import AlignIO
from pathlib import Path

print('usage: python split_align.py fastafile split_length')
input_file = Path(argv[1])
length = int(argv[2])
aln = AlignIO.read(input_file, 'fasta')
aln_len = len(aln[0])
for i in range(0, aln_len, length):
    filename = Path(f'{input_file.name}-{i}-{i+length}.fasta')
    print(filename)
    AlignIO.write(aln[:, i:i+length], filename, 'fasta')
