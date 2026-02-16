#!/usr/bin/python3

from pathlib import Path
from sys import argv
import gzip


def split(raw, number):
    raw = Path(raw).absolute()
    splitted = raw.with_suffix(f".{number}").name
    splitted_handle = open(splitted, "wb")
    try:
        raw_handle = gzip.open(raw)
        raw_handle.read(10)
        raw_handle.seek(0)
    except Exception:
        raw_handle = open(raw, "rb")
    line = iter(raw_handle)
    count = 0
    while count < number:
        # four line one record
        try:
            splitted_handle.write(next(line))
            splitted_handle.write(next(line))
            splitted_handle.write(next(line))
            splitted_handle.write(next(line))
        except StopIteration:
            break
        count += 1
    raw_handle.close()
    splitted_handle.close()
    return splitted, count


raw, number = argv[1:]
split(raw, int(number))
