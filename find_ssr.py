#!/usr/bin/python3

from sys import argv
from Bio import SeqIO
from timeit import default_timer as timer
import re

start = timer()
pattern = re.compile(r'([ATCG][ATCG]?[ATCG]?[ATCG]?[ATCG]?[ATCG]?)\1{2,}')
found = 0
with open(argv[1], 'r') as raw, open(argv[1]+'.ssr', 'w') as out:
    out.write('id,unit,unit_len,times,start,sequence\n')
    for record in SeqIO.parse(raw, 'fasta'):
        # finditer can return group(0), findall cannot
        for i in re.finditer(pattern, str(record.seq)):
            found += 1
            out.write('{},{},{},{},{},{}\n'.format(
                record.id,
                i.group(1),
                len(i.group(1)),
                len(i.group(0))//len(i.group(1)),
                i.start(),
                i.group(0)))
end = timer()
print('Cost {:.2f} seconds.'.format(end-start))
print('Found {} SSRs.'.format(found))
