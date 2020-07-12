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
    def is_root(clade):
        if clade == root:
            return 'is_root'
        else:
            return 'not_root'

    for t in trees:
        tree = Phylo.read(t, 'newick').as_phyloxml()
        root = tree.root
        print()
        print('tree, type, group, confidence')
        for type_ in info:
            color = ['orange', 'green', 'blue', 'red']
            mrcas = dict()
            for group in info[type_]:
                taxons = []
                for i in info[type_][group]:
                    clade = list(tree.find_clades(i))
                    if len(clade) == 0:
                        # print(i, 'not found')
                        pass
                    else:
                        taxons.append(clade[0])
                        clade[0].color = color[-1]
                try:
                    purple = [i for i in tree.get_nonterminals() if
                              i.color=='#992299']
                    print(purple)
                    mrca = tree.common_ancestor(*taxons)
                    mrca.color = '#992299'
                    # print(group, mrca!=tree.root, tree.get_path(mrca))
                # Bio.Phylo seems raise TypeError when mrca not found
                except Exception:
                    mrca = None
                    print(f'MRCA of {group} in {type_} not found in {t}.')
                    raise
                mrcas[group] = mrca
                color.pop()
            Phylo.draw(tree)
            mrcas_set = set(mrcas.values())
            if None in mrcas_set or len(mrcas_set) == 1:
                print('####', mrcas_set)
                continue
            else:
                for g in mrcas:
                    print(t, type_, g, is_root(mrcas[g]), mrcas[g].confidence)


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
    trees = list(arg.folder.glob('*'))
    info = parse_info(arg)
    types = [arg.folder/i for i in info.keys()]
    # for i in types:
    #     i.mkdir()
    divide_trees(trees, info, types)


if __name__ == '__main__':
    main()
