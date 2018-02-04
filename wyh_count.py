#!/usr/bin/python3

import re

pattern = re.compile(r'/(\d+_\d?).*:(\d+)')
with open('./its.log', 'r') as _:
    raw = re.findall(pattern, _.read())
    its = {i[0]: i[1] for i in raw}
with open('./matk.log', 'r') as _:
    raw = re.findall(pattern, _.read())
    matk = {i[0]: i[1] for i in raw}
with open('./rbcl.log', 'r') as _:
    raw = re.findall(pattern, _.read())
    rbcl = {i[0]: i[1] for i in raw}
sample = matk.keys() | rbcl.keys() | its.keys()
sample_dict = {i: [0, 0, 0] for i in sample}
for index, gene in enumerate([matk, rbcl, its]):
    for item in gene:
        sample_dict[item][index] += 1
result = list()
for i in sample_dict.keys():
    no_1, no_2 = i.split('_')
    if no_2 == '':
        no_2 = 0
    else:
        no_2 = int(no_2)
    no_1 = int(no_1)
    result.append([i, *sample_dict[i], no_1, no_2])

result.sort(key=lambda x: (x[-2], x[-1]))
with open('result.csv', 'w') as out:
    out.write('Sample,matK,rbcL,ITS\n')
    for i in result:
        out.write('{},{},{},{}\n'.format(i[0], i[1], i[2], i[3]))
