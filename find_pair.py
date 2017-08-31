#!/usr/bin/python3

from Bio import SeqIO
from sys import argv

print('Usage: python3 find_pair.py read_you_want_to_find.fastq'
    'another_direction.fastq')

description = set()
found = list()
for i in SeqIO.parse(argv[1], 'fastq'):
    description.add(i.id)

n = 0
for i in SeqIO.parse(argv[2], 'fastq'):
    if i.id in description:
        n += 1
        found.append(i)
        description.remove(i.id)
        print('Found {} sequences'.format(n))

with open('found.fastq', 'w') as out:
    SeqIO.write(found, out, 'fastq')
