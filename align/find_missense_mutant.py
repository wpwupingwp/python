#!/usr/bin/python3
from pathlib import Path
from sys import argv
import numpy as np
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


def main():
    # a = Path('CDS-rpoB.aa.aln')
    input_file = Path(argv[1])
    output_file = input_file.with_suffix('.csv')
    output_file2 = input_file.with_suffix('.select.aln')
    output = open(output_file, 'w')
    output2 = open(output_file2, 'w')
    out3 = set()
    name, seqs = fasta_to_array(input_file)
    row, col = seqs.shape
    threshold = row // 2
    for a in range(row):
        a_seq = seqs[a]
        for b in range(a + 1, row):
            b_seq = seqs[b]
            equal = (a_seq == b_seq)
            missense = set()
            begin = False
            span = [-1, -1]
            for j in range(1, col):
                if equal[j] != equal[j - 1]:
                    if not begin:
                        begin = True
                        span[0] = j
                    else:
                        begin = False
                        span[1] = j
                        missense.add(tuple(span))
                        span = [-1, -1]
            if len(missense) == 1:
                loc = slice(*missense.pop())
                a_s = a_seq[loc]
                b_s = b_seq[loc]
                if '-' not in a_s and '-' not in b_s:
                    type_ = 'mutant'
                else:
                    type_ = 'indel'
                out_line = '\t'.join([name[a][0], name[b][0],
                                     f'{loc.start + 1}-{loc.stop}', type_,
                                     f'{a_s[0]}>{b_s[0]}'])
                print(out_line)
                out3.add(name[a][0])
                out3.add(name[b][0])
                output.write(out_line + '\n')
    for i in out3:
        output2.write('>'+i+'\n')
        output2.write(''.join(seqs[np.where(name==i)[0][0], :])+'\n')
    print(out3)
    return


if __name__ == '__main__':
    main()