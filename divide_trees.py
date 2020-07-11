#!/usr/bin/python3

import argparse
import logging
from pathlib import Path


def parse_info(arg):
    """
    Format of info file:
    Type1
    A: taxon1 taxon2 taxon3
    B: taxon4 taxon5 taxon6
    Type2
    A: taxon7 taxon8 taxon9
    B: taxon4 taxon5 taxon6
    Type3
    A: taxon1 taxon2 taxon3
    B: taxon8 taxon9 taxon10
    """
    info = dict()
    with open(arg.info) as raw:
        for line in raw:
            if line.startswith('Type'):
                type_name = line.strip()
                info[type_name] = dict()
                continue
            group_name, *taxon = line.strip().split(' ')
            group_name = group_name.split(':')[0]
            if not isinstance(taxon, list):
                taxon = [taxon, ]
            info[type_name][group_name] = taxon
        info[type_name][group_name] = taxon
    return info


def function():
    pass


def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('-info', required=True,
                     help='info of taxons to be clusterd')
    arg.add_argument('-folder', required=True, help='folder contains trees')
    arg.print_usage()
    print(parse_info.__doc__）
    return arg.parse_args()


def main():
    """
    Divide trees according to type of topology.
    """
    arg = parse_args()
    arg.out = Path(arg.out)
    # start here
    function()
    # end


if __name__ == '__main__':
    main()
