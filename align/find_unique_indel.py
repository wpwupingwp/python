#!/usr/bin/python3
from pathlib import Path
import logging
import numpy as np

log = logging.getLogger("__main__")
log.setLevel(logging.INFO)


def fasta_to_array(aln_fasta: Path) -> (np.array, np.array):
    data = []
    record = ["id", "sequence"]
    with open(aln_fasta, "r", encoding="utf-8") as raw:
        for line in raw:
            if line.startswith(">"):
                data.append([record[0], "".join(record[1:])])
                # remove ">" and CRLF
                name = line[1:].strip()
                record = [name, ""]
            else:
                record.append(line.strip().upper())
        # add last sequence
        data.append([record[0], "".join(record[1:])])
    # skip head['id', 'seq']
    data = data[1:]
    # check sequence length
    length_check = [len(i[1]) for i in data]
    if len(set(length_check)) != 1:
        log.info(f"Invalid alignment file {aln_fasta}")
        return None, None
    # remove duplicated
    seq_id = {i[1]: i[0] for i in data}
    seq_id_tuple = tuple(seq_id.items())
    log.info(f"{len(data) - len(seq_id_tuple)} duplicated seqs.")
    # Convert List to numpy array.
    # order 'F' is a bit faster than 'C'
    # new = np.hstack((name, seq)) -> is slower
    name_array = np.array([[i[1]] for i in seq_id_tuple], dtype=str)
    # fromiter is faster than from list
    # S1: bytes
    sequence_array = np.array(
        [np.fromiter(i[0], dtype=np.dtype("U1")) for i in seq_id_tuple], order="F"
    )
    if name_array is None:
        log.error("Bad fasta file {}.".format(aln_fasta))
    return name_array, sequence_array


a = Path("CDS-rpoB.fasta.aln")
names, seqs = fasta_to_array(a)
row, col = seqs.shape
gaps_row = np.count_nonzero(seqs == "-", axis=1)
#
indels = set()
for i in range(row):
    if gaps_row[i] == 0:
        continue
    seq = seqs[i]
    is_gap = seq == "-"
    begin = False
    span = [-1, -1]
    for j in range(1, col):
        if is_gap[j] != is_gap[j - 1]:
            if not begin:
                begin = True
                span[0] = j
            else:
                begin = False
                span[1] = j
                if (span[1] - span[0]) % 3 == 0:
                    indels.add(tuple(span))
                span = [-1, -1]
fake_indel = set()
for i in indels:
    if np.count_nonzero(seqs[:, i[0] : i[1]] == "-") == 0:
        print(i, "fake")
        fake_indel.add(i)
indels.difference_update(fake_indel)
# missing 1-1
threshold = row // 2
for i in indels:
    region = seqs[:, i[0] : i[1]]
    for seq, index, count in zip(
        *np.unique(region, axis=0, return_index=True, return_counts=True)
    ):
        if count > threshold:
            continue
        type_ = "delete" if seq[0] == "-" else "insert"
        for j in range(row):
            if np.array_equal(region[j], seq):
                print(names[j][0], type_, i, count, "".join(seq))
