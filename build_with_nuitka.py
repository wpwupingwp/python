#!/usr/bin/python3
"""
# # install
```bash
python3 -m pip install nuitka==0.9.6
```
require c compilers

# build
 python37.exe -m nuitka .\arp_hap_to_nex.py --onefile --enable-plugin=tk-inter

"""

from subprocess import run
from sys import argv

r = run(
    f"python37 -m nuitka --standalone --show-progress "
    f"--nofollow-imports --enable-plugin=tk-inter {argv[1]} "
    f"--onefile --windows-disable-console --enable-plugin=numpy",
    shell=True,
)
