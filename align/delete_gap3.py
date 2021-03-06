#!/usr/bin/python3

from functools import wraps
from timeit import default_timer as timer
import argparse
import numpy as np


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


@print_time
def read(fasta):
    data = list()
    record = ['id', 'seq']
    with open(fasta, 'r') as raw:
        for line in raw:
            if line.startswith('>'):
                data.append([record[0], ''.join(record[1:])])
                name = line[1:-1]
                record = [name, ]
            else:
                record.append(line[:-1].upper())
        data.append([record[0], ''.join(record[1:])])
    data = data[1:]
    return data


@print_time
def convert(old):
    # order 'F' is a bit faster than 'C'
    # name = np.array([[i[0]] for i in old], dtype=np.bytes_)
    # seq = np.array([list(i[1]) for i in old], dtype=np.bytes_)
    # new = np.hstack((name, seq))
    new = np.array([list(i[1]) for i in old], dtype=np.bytes_)
    return new, new.shape


@print_time
def remove_gap(alignment, rows, columns):
    # alignment = rows(how many lines) * columns(how many columns)
    # get alignment head
    keep = [0, ]
    for index in range(1, columns):
        column = alignment[:, [index]]
        a = (column == b'A').sum()
        t = (column == b'T').sum()
        c = (column == b'C').sum()
        g = (column == b'G').sum()
        gap = columns - a - t - c - g
        if gap == rows:
            print('Empty in column {}'.format(index))
            print(gap, a, t, c, g, columns)
        elif (a+1 == (rows) or t+1 == (rows) or c+1 == rows or
              g+1 == (rows)):
            print('Only one in column {}'.format(index))
        elif a == rows or t == rows or c == rows or g == rows:
            print('All same in column {}'.format(index))
        else:
            keep.append(index)
            # short = np.hstack((short, column))
    keep = np.array(keep)
    short = alignment[:, keep]
    shape = list(short.shape)
    if len(shape) == 1:
        shape.append(1)
    return short, shape


@print_time
def write(data, output_file):
    with open(output_file, 'wb') as output:
        for i in data:
            seq_id, seq = i[0], i[1:]
            seq = b''.join(seq)
            output.write(b'>'+seq_id+b'\n'+seq+b'\n')


@print_time
def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('input', help='input alignment file')
    arg.add_argument('-o', '--output', default='new.fasta')
    # arg.print_help()
    return arg.parse_args()


@print_time
def main():
    arg = parse_args()
    alignment = read(arg.input)
    new, shape = convert(alignment)
    after_delete, new_shape = remove_gap(new, *shape)
    write(after_delete, arg.output)
    print('Remove {} columns.'.format(shape[1]-new_shape[1]))


if __name__ == '__main__':
    main()
