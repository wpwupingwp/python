#!/usr/bin/python3

from sys import argv

n = 1
with open(argv[1], "r") as old, open(argv[1] + ".number", "w") as new:
    for line in old:
        if line.startswith(">"):
            line = line.replace(">", ">No.{}|".format(n))
            n += 1
        new.write(line)
