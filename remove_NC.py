#!/usr/bin/python3

from Bio import SeqIO
from sys import argv

result = []
for record in SeqIO.parse(argv[1]):
    if not record.id.startswith('NC_'):
        result.append(record)
    else:
        print(record.id)
SeqIO.write(result, argv[1]+'.clean', 'gb')
