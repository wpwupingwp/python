#!/usr/bin/python3

from Bio import SeqIO
from sys import argv

new = list()
for record in SeqIO.parse(argv[1], 'fasta'):
    record.seq = record.seq.upper()
    new.append(record)
SeqIO.write(new, argv[1]+'.new', 'fasta')
