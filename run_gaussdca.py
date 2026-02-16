from juliacall import Main as jl
from sys import argv
from pathlib import Path
from typing import Iterable
import numpy as np


# multithread cause numpy failed to read from julia
print('Run: uv run python3 -X juliacall-threads=1 run_gaussdca.py protein.aln')
print('Add package: pkg> add "https://github.com/carlobaldassi/GaussDCA.jl"')
def parse_fasta(fasta_file: Path) -> Iterable[tuple[str, str]]:
    """
    Import from treebarcode.
    Upper letter
    Return tuple(title: str, sequence: str)
    """
    with open(fasta_file, 'r') as f:
        record: list[str] = []
        title = ''
        for line_raw in f:
            line = line_raw.strip()
            if line.startswith('>'):
                if len(record) != 0:
                    join_str = ''.join(record)
                    if len(join_str.strip()) != 0:
                        yield title, join_str.upper()
                    record.clear()
                title = line[1:]
            else:
                record.append(line)
        if len(record) != 0:
            join_str = ''.join(record)
            if len(join_str.strip()) != 0:
                yield title, join_str


def write_fasta(records: Iterable[tuple[str, str]], filename: Path) -> Path:
    # sequence is in one line, no truncated
    with open(filename, 'w') as f:
        for title, seq in records:
            f.write(f'>{title}\n')
            f.write(f'{seq}\n')
    return filename


def aln_to_array(records: Iterable[tuple[str, str]]) -> tuple[
    np.ndarray, np.ndarray]:
    records_ = list(records)
    name_array = np.array([i[0] for i in records_], dtype=np.str_)
    # S1 for 1 byte character, save more memory than 'U1' but
    # encode/decode is required
    seq_array = np.array(
        [np.fromiter(i[1], dtype=np.dtype('S1')) for i in records_])
    return name_array, seq_array

fasta = Path(argv[1]).resolve()
result = fasta.with_suffix('.txt')
co = fasta.with_suffix('.co.aln')
non_co = fasta.with_suffix('.non_co.aln')

name, old_seq = aln_to_array(parse_fasta(fasta))
jl.seval("using GaussDCA")
fnr = jl.gDCA(str(fasta))
# jl.printrank(str(result), fnr)
# convert from numpy.void
np_array = np.array([list(i) for i in fnr.to_numpy()])
threshold = 0
np_array[:, 0] -= 1
np_array2 = np_array[np_array[:2]>threshold]
co_index = set(np_array2[:, :2].flatten().astype(int))
non_co_index = set(np.arange(0, old_seq.shape[1])) - co_index
print(old_seq.shape[1], 'columns', np_array.shape[0], 'pairs',
      np_array2.shape[0], 'pairs big score',
      len(co_index), 'coevolution sites', 
      len(non_co_index), 'non-coevoled sites')
np.savetxt(result, np_array, fmt=['%d', '%d', '%.18e'])
write_fasta(zip(name, old_seq[:, list(co_index)]), co)
write_fasta(zip(name, old_seq[:, list(non_co_index)]), non_co)
print(result, co, non_co)
