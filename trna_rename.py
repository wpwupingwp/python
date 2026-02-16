#!/usr/bin/python3

from sys import argv
import re

pattern = re.compile(r"(trn(?P<letter>[A-Z]|fM)(?P<anticodon>\w\w\w))")
with open(argv[1], "r") as raw, open(argv[1] + ".new", "w") as out:
    for line in raw:
        new = re.sub(
            pattern,
            lambda match: "trn"
            + match.groupdict()["letter"]
            + "_"
            + match.groupdict()["anticodon"].upper(),
            line,
        )
        out.write(new)
