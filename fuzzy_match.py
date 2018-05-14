#!/usr/bin/python3

import regex as re
from sys import argv

tag = 'GTAGACTGCGTACC'
max_mismatch = 3
pattern = re.compile(r'({}){{e<={}}}'.format(tag, max_mismatch))
pattern2 = re.compile(r'^(\w{5})\1')
print('Seq,GoodBarcode,Mismatch,Start,End')
with open(argv[1], 'r') as raw:
    for line in raw:
        barcode = re.search(pattern2, line)
        if barcode is None:
            good_barcode = False
        else:
            good_barcode = True
        match = re.search(pattern, line, re.BESTMATCH)
        if match is None:
            mismatch = ''
            loc = ('', '')
        else:
            mismatch = sum(match.fuzzy_counts)
            loc = match.span()
        print(line[:-1], str(good_barcode), mismatch, *loc, sep=',')
