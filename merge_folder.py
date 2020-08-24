#!/usr/bin/python3

from pathlib import Path
from shutil import move
from sys import argv
from timeit import default_timer as timer
import asyncio


async def write_to(s, d):
    d.write(s.read())


async def merge_file(source, dest):
    with open(source, 'rb') as s, open(dest, 'ab') as d:
        await write_to(s, d)


def main():
    """
    Try to use asyncio.
    """
    start = timer()
    print('python3 merge_folder.py source dest')
    source_dir = Path(argv[1]).absolute()
    dest_dir = Path(argv[2]).absolute()
    sources = set(i.name for i in source_dir.glob('gene*'))
    dests = set(i.name for i in dest_dir.glob('gene*'))
    to_merge = dests.intersection(sources)
    to_move = dests.difference(sources)
    loop = asyncio.get_event_loop()
    for i in to_merge:
        source = source_dir / i
        dest = dest_dir / i
        loop.run_until_complete(merge_file(source, dest))
    for j in to_move:
        source = source_dir / j
        dest = dest_dir / j
        move(source, dest)
    end = timer()
    print(end-start, 'seconds')


main()
