#!/usr/bin/python3

from Bio import SeqIO
from glob import glob

for i in glob('*.fasta'):
    SeqIO.convert(i, 'fasta', i+'.new', 'fasta')
