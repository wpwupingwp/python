#!/usr/bin/python3

from sys import argv

n = 0
with open(argv[1], 'r') as old, open(argv[1]+'.number', 'w') as new:
    for line in old:
        if line.startswith('>'):
            line = line.replace('>', '>{}'.format(n))
        new.write(line)
