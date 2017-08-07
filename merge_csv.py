#!/usr/bin/python3


from glob import glob

all = dict()
files = glob('*.csv')
for index, csv in enumerate(files):
    info = dict()
    info['Sample'] = csv.replace('.csv', '')
    with open(csv, 'r') as raw:
        for line in raw:
            line = line.strip().split(',')
            info[line[0]] = line[1]
    for key in info:
        if key in all:
            all[key].append(info[key])
        else:
            all[key] = ['0'] * index
            all[key].append(info[key])

with open('output.tsv', 'w') as output:
    for key in all:
        output.write('{}\t{}\n'.format(key, '\t'.join(all[key])))
