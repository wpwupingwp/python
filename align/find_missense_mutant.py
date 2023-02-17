#!/usr/bin/python3

from Bio import SeqIO
from pathlib import Path
import numpy as np
from subprocess import run

import logging

log = logging.getLogger('__main__')
log.setLevel(logging.INFO)




def fasta_to_array(aln_fasta: Path) -> (np.array, np.array):
    data = []
    record = ['id', 'sequence']
    with open(aln_fasta, 'r', encoding='utf-8') as raw:
        for line in raw:
            if line.startswith('>'):
                data.append([record[0], ''.join(record[1:])])
                # remove ">" and CRLF
                name = line[1:].strip()
                record = [name, '']
            else:
                record.append(line.strip().upper())
        # add last sequence
        data.append([record[0], ''.join(record[1:])])
    # skip head['id', 'seq']
    data = data[1:]
    # check sequence length
    length_check = [len(i[1]) for i in data]
    print(length_check)
    if len(set(length_check)) != 1:
        log.info(f'Invalid alignment file {aln_fasta}')
        return None, None
    # remove duplicated
    seq_id = {i[1]: i[0] for i in data}
    seq_id_tuple = tuple(seq_id.items())
    log.info(f'{len(data) - len(seq_id_tuple)} duplicated seqs.')
    # Convert List to numpy array.
    # order 'F' is a bit faster than 'C'
    # new = np.hstack((name, seq)) -> is slower
    name_array = np.array([[i[1]] for i in seq_id_tuple], dtype=str)
    # fromiter is faster than from list
    # S1: bytes
    sequence_array = np.array(
        [np.fromiter(i[0], dtype=np.dtype('U1')) for i in seq_id_tuple],
        order='F')
    if name_array is None:
        log.error('Bad fasta file {}.'.format(aln_fasta))
    return name_array, sequence_array


a = Path('CDS-rpoB.fasta.aln')
b = nt2aa(a)
name, seqs = fasta_to_array(b)
#tmp.unlink()

print(name)
print(seqs)