#!/usr/bin/python3

from pathlib import Path
from subprocess import run
from multiprocessing import cpu_count

n_cpu = max(cpu_count()//2, 1)
files = list(Path('.').glob('*R1*.gz'))
pair = [(i, Path(str(i).replace('.R1.', '.R2.'))) for i in files]
print(*pair, sep='\n')
f, r = pair[0]
f_out, r_out = [i.with_suffix('.clean') for i in pair[0]]
# -i {forward} -I {reverse} -o {forward out} -O {reverse out}
# -A {do not cut adapter} -G {do not cut poly-G} -u {unqualified percent limt}
# -w {number of threads}
qc = run(f'fastp -i {f} -I {r} -o {f_out} -O {r_out} -A -G -u 30 -w {n_cpu}',
         shell=True)
