#!usr/python3

from sys import argv

assert len(argv) == 4, (
    'Usage: python3 join_fastq.py left right output')
left = open(argv[1], 'r')
right = open(argv[2], 'r')
merge = open(argv[3], 'w')
for a, b in zip(left, right):
    merge.write(a)
    a = left.readline()
    b = right.readline()
    merge.write(f'{a.strip()}{b}')
    a = left.readline()
    b = right.readline()
    merge.write(a)
    a = left.readline()
    b = right.readline()
    merge.write(f'{a.strip()}{b}')
