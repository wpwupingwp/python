#!/usr/bin/python3

from pathlib import Path
from shutil import move
from sys import argv
import asyncio


async def write_to(s, d):
    d.write(s.read())


async def merge_file(source, dest):
    with open(source, 'rb') as s, open(dest, 'ab') as d:
        await write_to(s, d)


async def main():
    """
    Try to use asyncio.
    """
    print('python3 amerge_folder.py source dest')
    source_dir = Path(argv[1]).absolute()
    dest_dir = Path(argv[2]).absolute()
    sources = set(i.name for i in source_dir.glob('*'))
    dests = set(i.name for i in dest_dir.glob('*'))
    to_merge = dests.intersection(sources)
    to_move = sources.difference(dests)
    for j in to_move:
        source = source_dir / j
        dest = dest_dir / j
        move(source, dest)
    for i in to_merge:
        source = source_dir / i
        dest = dest_dir / i
        asyncio.create_task(merge_file(source, dest))


asyncio.run(main())
