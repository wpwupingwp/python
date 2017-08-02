#!/usr/bin/python3

from sys import argv


info = list()
with open(argv[1], 'r') as raw:
    for line in raw:
        if line.startswith('<table'):
            break
    for line in raw:
        if line.strip().startswith('<tr>'):
            record = list()
            continue
        record.append(line.strip())
        if line.strip().startswith('</tr>'):
            info.append(record)
            continue

