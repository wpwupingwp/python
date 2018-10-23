#!/usr/bin/python3

from sys import argv
from Bio import SeqIO

with open(argv[1], 'r') as old, open(argv[1]+'.rc', 'w') as new:
    for record in SeqIO.parse(old):
        SeqIO.write(record.reverse_complement(), new, 'fasta')
