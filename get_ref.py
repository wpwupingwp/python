#!/usr/bin/python3

from glob import glob
from subprocess import run
from Bio import SeqIO


def get_id(string):
    new_str = string.split('-beijing')[0]
    gene, kingdom, order, family, genus, *_ = new_str.split('|')
    return new_str, order, family, genus


fasta_dict = SeqIO.to_dict(SeqIO.parse('/tmp/trnLF.uniq', 'fasta'))
a = list(glob('*filtered.fasta'))
for fasta in a:
    handle = open(fasta+'-merge.fasta', 'w')
    orders = set()
    families = set()
    genera = set()
    id_list = list()
    records = list(SeqIO.parse(fasta, 'fasta'))
    for record in records:
        blast_id, order, family, genus = get_id(record.id)
        id_list.append(blast_id)
        orders.add(order)
        families.add(family)
        genera.add(genus)
    if len(orders) != 1 or len(families) != 1:
        for i in records:
            SeqIO.write(i, handle, 'fasta')
            SeqIO.write(fasta_dict[get_id(i.id)[0]], handle, 'fasta')
        continue
    elif len(genera) != 1:
        i = records[0]
        blast_id, order, family, genus = get_id(i.id)
        run('python3 ~/git/rename/uniq.py -c 5'
            ' /tmp/trnLF_out/{}.fasta'.format(family), shell=True)
        handle.close()
        run('cat {} /tmp/trnLF_out/{}.fasta.uniq >> {}-merge.fasta'.format(
            fasta, family, fasta), shell=True)
        continue
    else:
        i = records[0]
        blast_id, order, family, genus = get_id(i.id)
        handle.close()
        run('cat {} /tmp/trnLF_out/{}.fasta >> {}-merge.fasta'.format(
            fasta, genus, fasta), shell=True)
