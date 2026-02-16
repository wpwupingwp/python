from sys import argv
from pathlib import Path

import a3mcat

fasta = Path(argv[1]).resolve()
a3m = fasta.with_suffix('.a3m')
with open(fasta, 'r') as _:
    header = _.readline().strip().lstrip('>')
    print(header)
data = a3mcat.MSAfasta.from_fasta_file(fasta)
a3m_data = data.to_a3m(query_header=header)
a3m_data.save(a3m)
print(a3m)


