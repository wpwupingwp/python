import re
from sys import argv
from Bio import SeqIO
from Bio.Seq import Seq

old = argv[1]
new = argv[1] + ".new"
pattern = re.compile(r"[^atcgATCGN]")
new_records = []
for record in SeqIO.parse(old, "fasta"):
    record.seq = Seq(re.sub(pattern, "N", str(record.seq)))
    new_records.append(record)
SeqIO.write(new_records, new, "fasta")
