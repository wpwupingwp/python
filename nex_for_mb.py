#!/usr/bin/python3

from sys import argv
import re
from Bio import AlignIO
from Bio.Alphabet import IUPAC


raw = AlignIO.read(argv[1], 'fasta', alphabet=IUPAC.ambiguous_dna)
pattern = re.compile(r'\W')
for i in raw:
    i.id = re.sub(pattern, '_', i.id)
    if len(i.id) >= 90:
        print('{} -> ID longer than 90, cut!'.format(i.id))
        i.id = i.id[:87] + '...'
AlignIO.write(raw, argv[1]+'.nex', 'nexus')
