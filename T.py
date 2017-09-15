#!/usr/bin/python3

import pandas
from sys import argv

index = 0
while True:
    try:
        raw = pandas.read_excel(argv[1], sheetname=index)
        t = raw.T
        t.to_csv('{}-{}.tsv'.format(argv[1], index), sep='\t')
        index += 1
    except:
        break
