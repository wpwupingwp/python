#!/usr/bin/python3

# Usage: python3 split_msa.py fastqfile id_value
# require more memory

from subprocess import run
from sys import argv
from Bio import SeqIO
from os import remove

raw = argv[1] + '.raw'
run(f'vsearch --cluster_size {argv[1]} --id {argv[2]} --msaout {raw}',
    shell=True)
all_cluster = []
cluster = []
for record in SeqIO.parse(raw, 'fasta'):
    if record.id == 'consensus':
        all_cluster.append(cluster)
        cluster = []
    else:
        cluster.append(record)
all_cluster.sort(key=len, reverse=True)
print(f'Split into {len(cluster)} files.')
print('Order by size (big to small).')
remove(raw)
topn = 4
for i, cluster in enumerate(all_cluster, 1):
    if topn < 0:
        break
    filename = argv[1] + f'.{i}'
    SeqIO.write(cluster, filename, 'fasta')
    if len(cluster) == 1:
        continue
    run(f'mafft --reorder --ep 1 {filename} > {filename}.aln',
        shell=True)
    topn -= 1
