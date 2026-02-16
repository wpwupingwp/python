from juliacall import Main as jl
from sys import argv
from pathlib import Path
import numpy as np

# multithread cause numpy failed to read from julia
print('Run: uv run python3 -X juliacall-threads=1 run_gaussdca.py protein.aln')
print('Add package: pkg> add "https://github.com/carlobaldassi/GaussDCA.jl"')
fasta = Path(argv[1]).resolve()
result = fasta.with_suffix('.txt')

jl.seval("using GaussDCA")
fnr = jl.gDCA(str(fasta))
# jl.printrank(str(result), fnr)
# convert from numpy.void
np_array = np.array([list(i) for i in fnr.to_numpy()])
print(np_array[0])
np_array[:, 0] -= 1
print(np_array[0])
np.savetxt(result, np_array, fmt=['%d', '%d', '%.18e'])
print(result)
