#!/usr/bin/python3
from glob import glob
from pathlib import Path
import logging
import numpy as np
import re

log = logging.getLogger('__main__')
log.setLevel(logging.INFO)


def x():
    pattern = re.compile(r'\w+(-{3,})\w+')
    result = []

    for i in glob('*.aln'):
        data = SeqIO.parse(i, 'fasta')
        seq_id = {str(i.seq): i.id for i in data}
        print(i, 'have', len(seq_id), 'seqs')
        for seq in seq_id:
            matches = re.finditer(pattern, seq)
            for match in matches:
                no_gap = seq[:match.start()] + seq[match.end():]
                print(no_gap)
                if no_gap in seq_id:
                    found = (i, seq_id[seq], seq_id[no_gap])
                    print(found)

    with open('count.txt', 'w') as o:
        for i in result:
            o.write(f'{i[0]},{i[1]},{i[2]}\n')
    return


#%%
def fasta_to_array(aln_fasta: Path) -> (np.array, np.array):
    """
    Given fasta format alignment filename, return a numpy array for sequence:
    Faster and use smaller mem.
    Ensure all bases are capital.
    Args:
        aln_fasta(Path): aligned fasta file
    Returns:
        name(np.array): name array
        sequence(np.array): sequence array
    """
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
    if len(set(length_check)) != 1:
        log.info(f'Invalid alignment file {aln_fasta}')
        return None, None
    # remove duplicated
    seq_id = {i[1]: i[0] for i in data}
    seq_id_tuple = tuple(seq_id.items())
    log.info(f'{len(data)-len(seq_id_tuple)} duplicated seqs.')
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


a = 'CDS-rpoB.fasta.aln'
names, seqs = fasta_to_array(a)
row, col = seqs.shape
gaps_row = np.count_nonzero(seqs=='-', axis=1)
#
indels = set()
for i in range(row):
    if gaps_row[i] == 0:
        continue
    seq = seqs[i]
    is_gap = (seq=='-')
    begin = False
    span = [-1, -1]
    for j in range(1, col):
        if is_gap[j] != is_gap[j-1]:
            if not begin:
                begin = True
                span[0] = j
            else:
                begin = False
                span[1] = j
                if (span[1] - span[0]) % 3 == 0:
                    indels.add(tuple(span))
                span = [-1, -1]

for i in indels:
    print(i)

def y():
    gaps_col = np.count_nonzero(seqs=='-', axis=0)
    indel_type = gaps_col.copy().astype('U1')
    # I: someone insert a region, D: someone delete a regin, N: we're same
    indel_type[gaps_col!=0] = 'I'
    indel_type[(0<gaps_col) & (gaps_col<=n_unique//2)] = 'D'
    indel_type[0==gaps_col] = 'N'
    indels = []
    #len(indel_type) = seqs.shape[1]
    begin = False
    extend = False
    span = [-1, -1]
    for i in range(1, len(indel_type)):
        if indel_type[i] != indel_type[i-1]:
            if not begin:
                begin = True
                span[0] = i + 1
            else:
                begin = False
                span[1] = i + 1
                if (span[1] - span[0]) % 3 == 0:
                    indels.append((span, indel_type[i]))
                span = [-1, -1]

    print(indels)

