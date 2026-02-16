#!/usr/bin/python3
# require internet to init
# docker run -it -v ~/.pycorrector:/root/.pycorrector -v data:/data shibing624/pycorrector:0.0.2
# data folder for input/output
from timeit import default_timer as timer
import pycorrector as p


start = timer()
raw = open("/data/manuscript.txt", "r", encoding="utf-8")
out = open("/data/output.txt", "w", encoding="utf-8")
for line in raw:
    corrected, detail = p.correct(line.strip())
    out.write(corrected.strip() + "\n")
    for i in detail:
        if len(i) == 4:
            out.write("{},{},{}-{}\t".format(*i))
            out.write("\n")
end = timer()
print(end - start, "seconds.")
