#!/usr/bin/python3

import csv
import re
import sys

from copy import deepcopy

Value = list()
Value2 = list()
Row = list()
Out = list()
Fna = sys.argv[1]
List = sys.argv[2]
area = Fna.replace('.fna', '')
with open(Fna, 'r') as In:
    Raw = In.read()
with open(List, 'r') as List:
    Rows = List.read().split(sep='\n')
Rows.sort()
Rows.pop(0)
Line = ['{:03d}'.format(n) for n in range(141)]
Line[0] = area
Out.append(Line)
fill = [0 for n in range(140)]
for n in range(len(Rows)):
    if Rows[n] != '':
        Add = [Rows[n], area]
        Add.extend(fill)
        Out.append(Add)
Out2 = deepcopy(Out)
# one species
Id = re.findall('(?<=\>\d{2}-)[A-Z][a-z]+-\d{3}', Raw)
#                   >10        - E     ricales-001  
#                    area      - Species      -gene
for record in Id:
    toadd = (str(record)).split(sep='-')
    if not toadd in Value:
        Value.append(toadd)
Value.sort()
for item in Value:
    if item[0] in Rows:
        x = Line.index(item[1]) + 1
        y = Rows.index(item[0]) + 1
        Out[y][x] = 1
handle1 = open(''.join([Fna.replace('.fna', ''), '-1.csv']), 'w')
writer = csv.writer(handle1)
for line in Out:
    writer.writerow(line)
# two species
Id2 = re.findall('(?<=\>\d{2}-)[A-Z][a-z]+-[A-Z][a-z]+-\d{3}', Raw.replace('_', '-'))
for record in Id2:
    toadd = (str(record)).split(sep='-')
    if not toadd in Value2:
        Value2.append(toadd)
Value2.sort()
for item in Value2:
    x = Line.index(item[2]) + 1
    y = Rows.index(item[0]) + 1
    z = Rows.index(item[1]) + 1
    if Out[y][x] == 1:
        Out2[z][x] = 1
    elif Out[z][x] == 1:
        Out2[y][x] = 1
    elif Out[y][x] == '0' and Out[z][x] == '0':
        Out2[y][x] = 0.5
        Out2[z][x] = 0.5
handle2 = open(''.join([Fna.replace('.fna', ''), '-2.csv']), 'w')
writer2 = csv.writer(handle2)
for line in Out2:
    writer2.writerow(line)
