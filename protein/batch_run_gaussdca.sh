#!/bin/bash
#uv run python3 -X juliacall-threads=1 ./get_coevo_site.py ./t2.aln
for i in `ls species2/*.aln`
do
    uv run python3 -X juliacall-threads=1 ./run_gaussdca.py $i
done

