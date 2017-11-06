#!/usr/bin/python3

from Bio import SeqIO
from sys import argv

old = list(SeqIO.parse(argv[1], 'fasta'))
new = old[0:4]
SeqIO.write(new, argv[1]+'.new', 'fasta')
