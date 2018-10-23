#!/usr/bin/python3

import re
from sys import argv

pattern = re.compile(r'^>centroid.*;(?=size)')
n = 1
with open(argv[1], 'r') as old, open(argv[1]+'.rename', 'w') as new:
    for line in old:
        if line.startswith('>'):
            new.write(re.sub(pattern, '>{}-'.format(n), line))
            n += 1
        else:
            new.write(line)
