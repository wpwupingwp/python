#!/usr/bin/python3

from sys import argv
from collections import Counter
import re

pattern = re.compile(r'ATCG.{20}GTTTA')
data = list()

with open(argv[1], 'r') as fastq:
    for line in fastq:
        found = re.findall(pattern, line)
        if len(found) == 0:
            continue
        else:
            data.extend(found)

count = Counter(data)
with open('output.txt', 'w') as out:
    for key, value in count.items():
        out.write('{}\t{}\n'.format(key, value))
