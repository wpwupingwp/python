#!/usr/bin/python3

from sys import argv
from pathlib import Path

type_dict = dict()
input_file = Path(argv[1])
handle = open(input_file, "r")
for line in handle:
    if line.startswith("#") or line.startswith("scaffold"):
        continue
    else:
        line_split = line.strip().split("\t")
        feature_type = line_split[2]
        if feature_type == "scaffold":
            continue
        if feature_type in type_dict:
            output_file = type_dict[feature_type]
        else:
            output_filename = input_file.with_suffix("." + feature_type)
            output_file = open(output_filename, "a")
            type_dict[feature_type] = output_file
        # gff to bed
        out_line = "{}\t{}\t{}\t{}\t{}\t{}\n".format(
            line_split[0],
            int(line_split[3]) - 1,
            int(line_split[4]) - 1,
            line_split[8],
            line_split[5],
            line_split[6],
        )
        output_file.write(out_line)
