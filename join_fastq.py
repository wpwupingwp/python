﻿#!/usr/bin/python3


from Bio import SeqIO
import sys

left = SeqIO.parse(sys.argv[1], 'fastq')
right = SeqIO.parse(sys.argv[2], 'fastq')
handle = open('combine.fastq', 'w')
offset = 32
for l, r in zip(left, right):
    l_seq = str(l.seq)
    r_seq = str(r.seq.reverse_complement())
    l_qual = ''.join([chr(i+offset) for i in l.letter_annotations[
        'phred_quality']])
    r_qual = ''.join([chr(i+offset) for i in r.letter_annotations[
        'phred_quality']])
    length = 500 - len(l_seq) - len(r_seq)
    sequence = '{}{}{}'.format(l_seq, 'N'*length, r_seq)
    quality = '{}{}{}'.format(l_qual, 'A'*length, r_qual[::-1])
    name = l.description
    handle.write('@{0}\n{1}\n+\n{2}\n'.format(name, sequence, quality))

print('Done.')
