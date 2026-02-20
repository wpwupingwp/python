"""
1. no mutant
2. 1st mutant
3. 2nd mutant
4. both mutant
"""
from sys import argv
from pathlib import Path
import numpy as np

from run_gaussdca import parse_fasta, aln_to_array, array_to_fasta, write_fasta


def find_seqs(a, b, name, seq):
    seq_other = np.delete(seq, [a, b], axis=1)
    new_seq, count = np.unique(seq_other, return_counts=True, axis=0)
    other_same_seq = new_seq[np.argmax(count)]
    same_mask = np.all(seq_other == other_same_seq, axis=1)
    same_name = name[same_mask]
    same_seq = seq[same_mask]
    return same_name, same_seq


def main():
    print('Usage: python predict_co_site.py fasta_file.fasta dca_result.txt')
    raw_aln_file = Path(argv[1]).resolve()
    dca_file = Path(argv[2]).resolve()

    raw_name, raw_seq = aln_to_array(parse_fasta(raw_aln_file))
    unique_seq, unique_index = np.unique(raw_seq, return_index=True, axis=0)
    unique_name_ = raw_name[unique_index]

    n_gaps = np.sum(unique_seq==b'-', axis=0)
    no_gap_index = np.where(n_gaps == 0)[0]
    no_gap_seq = unique_seq[no_gap_index]
    no_gap_name = unique_name_[no_gap_seq]

    dca_array = np.loadtxt(dca_file)
    top_n = 10
    dca_top = dca_array[:top_n]
    for record in dca_top:
        a, b, score = record
        if a > b:
            a, b = b, a
        a = int(a)
        b = int(b)
        if a == 0 or b == raw_seq.shape[1]:
            print('bad index', record)
            continue
        filename = raw_aln_file.with_suffix(f'.{a}-{b}.aln')
        name, seq = find_seqs(a, b, no_gap_name, no_gap_seq)
        if name:
            array_to_fasta(name, seq, filename)
    return


if __name__ == '__main__':
    main()
