#!/usr/bin/python3

from Bio import SeqIO
from sys import argv


print('python3 split_ref.py file format')
for index, record in enumerate(SeqIO.parse(argv[1], argv[2])):
    out = f'{argv[1]}.{index}'
    SeqIO.write(record, out, argv[2])
