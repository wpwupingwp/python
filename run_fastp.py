#!/usr/bin/python3

from pathlib import Path
from subprocess import run
from multiprocessing import cpu_count

n_cpu = max(cpu_count() // 2, 1)
files = list(Path(".").glob("*R1*.gz"))
pair = [(i, Path(str(i).replace(".R1.", ".R2."))) for i in files]
for i in pair:
    f, r = i
    f_out, r_out = [j.with_suffix(".clean") for j in i]
    h_report = f.with_suffix(".html")
    j_report = f.with_suffix(".json")
    # -i {forward} -I {reverse} -o {forward out} -O {reverse out}
    # -A {do not cut adapter} -G {do not cut poly-G} -u {unqualified percent limit}
    # -w {number of threads} -h {html report file} -j {json report file}
    qc = run(
        f"fastp -i {f} -I {r} -o {f_out} -O {r_out} -A -G -u 30 "
        f"-w {n_cpu} -h {h_report} -j {j_report}",
        shell=True,
    )
