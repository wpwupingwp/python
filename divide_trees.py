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

    def get_mrca(names):
        clades = set()
        for i in names:
            clade = list(tree.find_clades(i))
            if clade:
                clades.add(clade[0])
        mrca = tree.common_ancestor(*clades)
        return clades, mrca

    def get_parent(root, clade):
        if clade == root:
            return root
        lineage = root.get_path(clade)
        return lineage[-2]

    def like_monophyletic(lists):
        # biopython's same-name function is too strict
        result = {}
        for list_ in lists:
            copy = lists[::]
            copy.remove(list_)
            children = list_[1].get_terminals()
            others = []
            for c in copy:
                group, mrca, clades = c
                # only consider given group's terminals
                others.extend(clades)
            if len(set(children) & set(others)) == 0:
                result[list_[0]] = True
            else:
                result[list_[0]] = False
        return result

    results = []
    for t in trees:
        tree = Phylo.read(t, 'newick').as_phyloxml()
        root = tree.root
        print()
        for type_ in info:
            ok = ''
            color = ['orange', 'green', 'blue', 'red']
            terminals = []
            mrcas = {}
            for group in info[type_]:
                clades, mrca = get_mrca(info[type_][group])
                for clade in clades:
                    clade.color = color[-1]
                color.pop()
                terminals.append([group, mrca, clades])
                mrcas[group] = mrca
            result = like_monophyletic(terminals)
            for group in result:
                if result[group]:
                    results.append([t, type_,  mrcas[group].confidence.value])
                    ok = ' OK'
            Phylo.draw(tree, do_show=False, title=(type_+ok,),
                       savefig=(t.with_suffix('.pdf'),))
    return results


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
    trees = [i.absolute() for i in trees]
    info = parse_info(arg)
    types = [arg.folder/i for i in info.keys()]
    types_dict = dict(zip(info.keys(), types))
    for i in types:
        i.mkdir()
    result = divide_trees(trees, info, types)
    result_csv = arg.folder / 'result.csv'
    with open(result_csv, 'w') as out:
        out.write('Tree,Type,Confidence\n')
        for i in result:
            out.write('{},{},{}\n'.format(*i))
            Path(types_dict[i[1]]/i[0]).write_bytes(i[0].read_bytes())


if __name__ == '__main__':
    main()
