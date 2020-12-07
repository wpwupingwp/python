#!/usr/bin/python3

import argparse
from functools import wraps
from timeit import default_timer as timer
from Bio import SeqIO


def print_time(function):
    @wraps(function)
    def wrapper(*args, **kargs):
        start = timer()
        result = function(*args, **kargs)
        end = timer()
        print('The function {0} Cost {1:3f}s.\n'.format(
            function.__name__, end-start))
        return result
    return wrapper


def shorten(fasta, max_len):
    output = open(fasta+'.short', 'w')
    for record in SeqIO.parse(fasta, 'fasta'):
        if len(record) < max_len:
            SeqIO.write(record, output, 'fasta')
        else:
            print(record.id, len(record))


def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('input', help='input fasta file')
    arg.add_argument('-l', type=int, default=10000,
                     help='maximum length, default 10000')
    # arg.print_help()
    return arg.parse_args()


def main():
    """docstring
    """
    arg = parse_args()
    # start here
    shorten(arg.input, arg.l)
    # end


if __name__ == '__main__':
    main()
