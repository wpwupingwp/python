#!/usr/bin/python3

# Usage: python3 split_msa.py fastqfile id_value

from subprocess import run
from sys import argv
from Bio import SeqIO
from os import remove

n = 1
fasta = 'tmp.fasta'
cluster = 'cluster.fasta'
run(f'vsearch --cluster_size {argv[1]} --id {argv[2]} --msaout {cluster}',
    shell=True)
handle = open(fasta, 'w')
for record in SeqIO.parse(cluster, 'fasta'):
    if record.id == 'consensus':
        handle.close()
        run(f'mafft --ep 1 {fasta} > {argv[1]}.{n}',
            shell=True)
        n += 1
        handle = open(fasta, 'w')
    else:
        SeqIO.write(record, handle, 'fasta')
print(f'Split into {n-1} files.')
handle.close()
remove(fasta)
remove(cluster)
