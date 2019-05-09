#!/usr/bin/python3

from Bio import AlignIO
from Bio.Alphabet import IUPAC
from Bio.Nexus import Nexus

from glob import glob
import argparse


def get_format(arg):
    with open(arg.input[0], 'r') as _:
        head = _.raedline()
        if head.lower().startswith('#nexus'):
            return 'nexus'
        elif head.startswith('>'):
            return 'fasta'
        else:
            exit('Unsupport format. Only accept fasta or nexus')


def convert(arg):
    nexus_files = []
    for i in arg.input:
        AlignIO.convert(i, 'fasta', i+'.nexus', 'nexus',
                        alphabet=IUPAC.ambiguous_dna)
        nexus_files.append(i)
    arg.input = nexus_files
    return arg


def clean_name(name):
    return name.replace('.fasta', '').replace('.nexus', '')


def combine(arg):
    file_format = get_format(arg)
    if file_format == 'fasta':
        arg = convert(arg)
    name_data = [(clean_name(name), Nexus.Nexus(name)) for name in arg.input]
    combined = Nexus.combine(name_data)
    combined.write_nexus_data(filename=arg.output)


def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('input', '-i', nargs='+', help='input file/files')
    arg.add_argument('output', '-o', help='output file')
    parsed = arg.parse_args()
    # allow asterisk
    if len(arg.input) == 1:
        parsed.input = list(glob(arg.input))
    return parsed


def main():
    """
    Convert files between fasta, gb, nexus and phylip format.
    """
    arg = parse_args()
    combine(arg)
    print('Finished.')
    print('{} files were combined.'.format(len(arg.input)))


if __name__ == '__main__':
    main()
