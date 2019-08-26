#!/usr/bin/python3

from Bio import SeqIO
from sys import argv


for record in SeqIO.parse(argv[1], 'fasta'):
    print(record.id, len(record))
