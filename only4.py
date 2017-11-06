#!/usr/bin/python3

from Bio import SeqIO
from sys import argv

old = list(SeqIO.parse(argv[1], 'fasta'))
new = old[0:int(argv[2])]
SeqIO.write(new, argv[1]+'.new', 'fasta')
