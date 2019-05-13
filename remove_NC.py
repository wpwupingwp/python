#!/usr/bin/python3

from Bio import SeqIO
from sys import argv
from collections import defaultdict

result = []
name_id = defaultdict(list)
id_name = {}
exclude = []
n = 0
for record in SeqIO.parse(argv[1], 'gb'):
    name_id[record.annotations['organism']].append(record.id)
    id_name[record.id] = record.annotations['organism']
    n += 1
for key in name_id:
    if len(name_id[key]) == 1:
        continue
    else:
        for value in name_id[key]:
            if value.startswith('NC_'):
                exclude.append(value)
for record in SeqIO.parse(argv[1], 'gb'):
    if record.id not in exclude:
        result.append(record)
    else:
        organism = id_name[record.id]
        print('Remove {} from {}: {}'.format(
            record.id, organism, name_id[organism]))

SeqIO.write(result, argv[1]+'.clean', 'gb')
print('{} of {} left.'.format(n, len(result)))
