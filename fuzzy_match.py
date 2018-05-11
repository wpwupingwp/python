#!/usr/bin/python3

import regex as re
from sys import argv

tag = 'GTAGACTGCGTACC'
max_mismatch = 3
pattern = re.compile(r'({}){{e<={}}}'.format(tag, max_mismatch))
print('Seq,Mismatch,Start,End')
with open(argv[1], 'r') as raw:
    for line in raw:
        for match in re.finditer(pattern, line):
            mismatch = sum(match.fuzzy_counts)
            loc = match.span()
            print(line[:-1], mismatch, *loc, sep=',')
