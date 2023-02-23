#!/usr/bin/python3
from Bio import SeqIO
from sys import argv
import requests

url = 'https://api.esmatlas.com/foldSequence/v1/pdb'

for record in SeqIO.parse(argv[1], 'fasta'):
    _ = record.id.split('|')
    name = '_'.join([_[0], _[6], _[7], _[8]])
    seq = str(record.seq)
    r = requests.post(url, seq)
    if r.status_code == 200:
        with open(name+'.pdb', 'w') as out:
            out.write(r.text)
        print('Got', name)
    else:
        print('Fail', name, r.status_code, r.text)
