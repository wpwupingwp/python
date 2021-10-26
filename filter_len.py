#!/usr/bin/python3

from sys import argv
from pathlib import Path
from Bio import SeqIO


print('Usage: python filter_len.py fastafile length_range')
print('Example: python filter_len.py rbcL.fasta 100-200')
print('Example: python filter_len.py rbcL.fasta min-100 101-1000 1001-10000 '
      '10001-200000 200000-max')

fasta = Path(argv[1]).absolute()
length_range_raw = argv[2:]
range_file = dict()
for i in length_range_raw:
    r = i.split('-')
    if len(r) != 2:
        raise ValueError('Bad range format')
    if r[0] == 'min':
        r[0] = 0
    if r[1] == 'max':
        r[1] = 10000000000
    r_ = range(int(r[0]), int(r[1]))
    filename = fasta.with_suffix(f'.{i}.fasta')
    handle = open(filename, 'a')
    range_file[r_] = handle
for record in SeqIO.parse(fasta, 'fasta'):
    length = len(record)
    for range_, handle in range_file:
        if length in range_:
            SeqIO.write(record, handle, 'fasta')
            break
    raise ValueError(f'{length} cannot be process')
print('Done')

