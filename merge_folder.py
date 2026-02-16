#!/usr/bin/python3

from pathlib import Path
from shutil import move
from sys import argv
from timeit import default_timer as timer


def merge_file(source, dest):
    with open(source, "rb") as s, open(dest, "ab") as d:
        d.write(s.read())


def main():
    """
    Try to use asyncio.
    """
    start = timer()
    print("python3 amerge_folder.py source dest")
    source_dir = Path(argv[1]).absolute()
    dest_dir = Path(argv[2]).absolute()
    sources = set(i.name for i in source_dir.glob("*"))
    dests = set(i.name for i in dest_dir.glob("*"))
    to_merge = dests.intersection(sources)
    to_move = sources.difference(dests)
    for j in to_move:
        source = source_dir / j
        dest = dest_dir / j
        move(source, dest)
    for i in to_merge:
        source = source_dir / i
        dest = dest_dir / i
        merge_file(source, dest)
    print("Cost", timer() - start, "seconds")


main()
