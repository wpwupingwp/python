#!/usr/bin/python3

import argparse
from pathlib import Path

from Bio import Phylo


def parse_info(arg):
    """
Format of info file:
Type1
A:,taxon1,taxon2,taxon3
B:,taxon4,taxon5,taxon6
Type2
A:,taxon7,taxon8,taxon9
B:,taxon4,taxon5,taxon6
Type3
A:,taxon1,taxon2,taxon3
B:,taxon8,taxon9,taxon10
    """
    info = dict()
    with open(arg.info) as raw:
        for line in raw:
            if line.startswith('Type'):
                type_name = line.strip()
                info[type_name] = dict()
                continue
            group_name, taxon = line.strip().split(' ')
            group_name = group_name.split(':')[0]
            taxon = taxon.split(',')
            if not isinstance(taxon, list):
                taxon = [taxon, ]
            info[type_name][group_name] = taxon
        info[type_name][group_name] = taxon
    return info


def divide_trees(trees, info, types):
    """
    Args:
        trees(list): tree files, Path()
        info(dict): info of types, groups and taxons
        types(list): list of Path() to output
    """
    for t in trees:
        tree = Phylo.read(t, 'newick')
        print()
        for type_ in info:
            mrcas = dict()
            for group in info[type_]:
                taxons = []
                for i in info[type_][group]:
                    clade = list(tree.find_clades(i))
                    if len(clade) == 0:
                        pass
                        # print('\t', i, 'not found')
                    else:
                        taxons.append(clade[0])
                try:
                    mrca = tree.common_ancestor(*taxons)
                # Bio.Phylo seems raise TypeError when mrca not found
                except Exception:
                    mrca = None
                    print(f'MRCA of {group} in {type_} not found in {t}.')
                    raise
                mrcas[group] = mrca
            mrcas_set = set(mrcas.values())
            print(mrcas_set)
            if None in mrcas_set or len(mrcas_set) == 1:
                continue
            else:
                for g in mrcas:
                    print(t, type_, g, mrcas[g]!=tree.root, mrcas[g].confidence)


def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('-info', required=True,
                     help='info of taxons to be clusterd')
    arg.add_argument('-folder', required=True, help='folder contains trees')
    arg.print_usage()
    print(parse_info.__doc__)
    return arg.parse_args()


def main():
    """
    Divide trees according to type of topology.
    """
    arg = parse_args()
    arg.folder = Path(arg.folder)
    trees = list(arg.folder.glob('*.tre'))
    info = parse_info(arg)
    types = [arg.folder/i for i in info.keys()]
    for i in types:
        i.mkdir()
    divide_trees(trees, info, types)


if __name__ == '__main__':
    main()
