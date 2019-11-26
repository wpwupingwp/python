#!/usr/bin/python3

from sys import argv
from matplotlib import pyplot as plt
from numpy import logspace
import re

length = list()
coverage = list()
pattern = re.compile(r'length_(\d+)_cov_(\d+\.\d+)$')
with open(argv[1], 'r') as raw:
    for line in raw:
        if line.startswith('>'):
            info = re.search(pattern, line)
            length.append(int(info.group(1)))
            coverage.append(float(info.group(2)))

index = range(1, len(length)+1)
fig = plt.figure()
plt.title('Length of contigs')
plt.xlabel('Length (bp)')
plt.ylabel('Count')
plt.xlim(50, 1e4)
plt.xscale('log')
plt.hist(length, bins=logspace(2, 4, base=10, num=100), color='blue', label='length')
plt.savefig(argv[1]+'-length.svg')

plt.title('Coverage of contigs')
plt.xlabel('Coverage (x)')
plt.ylabel('Count')
plt.xlim(50, 1e4)
plt.xscale('log')
plt.hist(coverage, bins=logspace(1, 6, base=10, num=100), color='red',
         label='coverage')
plt.savefig(argv[1]+'-length.svg')
        #ax2 = ax1.twinx()
