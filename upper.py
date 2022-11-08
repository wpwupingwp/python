#!/usr/bin/python3
from sys import argv


def old():
    from Bio import SeqIO

    new = list()
    for record in SeqIO.parse(argv[1], 'fasta'):
        record.seq = record.seq.upper()
        new.append(record)
    SeqIO.write(new, argv[1]+'.new', 'fasta')


def new():
    out = argv[1]+'.new'
    with open(old, 'r') as a, open(new, 'w') as b:
        for line in a:
            if not line.startswith('>'):
                line = line.upper()
            b.write(line)


new()
