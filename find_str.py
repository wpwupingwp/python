#!/usr/bin/python3

from sys import argv
from Bio import SeqIO
from timeit import default_timer as timer
import re

start = timer()
pattern = re.compile(r'([ATCG]{2,6})\1{8,20}')
found = 0
with open(argv[1], 'r') as raw, open('STR-'+argv[1], 'w') as out:
    for record in SeqIO.parse(raw, 'fasta'):
        # finditer can return group(0), findall cannot
        for i in re.finditer(pattern, str(record.seq)):
            found += 1
            out.write('{},{},{},{}\n'.format(
                record.id,
                i.group(0),
                i.group(1),
                len(i.group(0))//len(i.group(1))))
end = timer()
print('Cost {:.2f} seconds.'.format(end-start))
print('Found {} STRs.'.format(found))
