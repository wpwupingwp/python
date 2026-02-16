#!/usr/bin/python3
from sys import argv
from Bio import SeqIO
from subprocess import run
from pathlib import Path


def main(nt_file: Path) -> Path:
    _translate = []
    for i in SeqIO.parse(nt_file, "fasta"):
        i.seq = i.seq.replace("-", "")
        _translate.append(i.translate(id=i.id, description="", table=11))
    tmp = nt_file.with_suffix(".tmp")
    aa = nt_file.with_suffix(".aa.aln")
    SeqIO.write(_translate, tmp, "fasta")
    r = run(f"mafft --auto --reorder {tmp} > {aa}", shell=True)
    if r.returncode != 0:
        print(f"Align {nt_file} failed.")
    tmp.unlink()
    return aa


if __name__ == "__main__":
    main(Path(argv[1]))
