#!/bin/bash
#uv run python3 predict_co_site.py t2.aln t2.txt
for i in `ls species2/*.txt`
do
    uv run python3 predict_co_site.py ${i%.txt}.aln $i
done
