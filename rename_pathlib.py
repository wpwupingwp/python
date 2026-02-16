#!/usr/bin/python3

from pathlib import Path
import re

# remove string
pattern = re.compile(r"[\w]{5,}-")
# use **/* to find all gz
a = Path(".").glob("**/*.gz")
# add id to solve repeat filename
for i, j in enumerate(a):
    # if in current dir
    if j.parents[0] == Path("."):
        continue
    # skip rawdata
    if "Rawdata" in j.parts:
        print("Skip {}".format(j))
        continue
    new = re.sub(pattern, "", j.name)
    new_uniq = "{}-{}".format(i, new)
    # mv
    j.rename(Path(j.parts[0]).joinpath(new_uniq))
