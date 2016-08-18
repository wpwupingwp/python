#!/usr/bin/python3

import argparse
from Bio import SeqIO

parameters = argparse.ArgumentParser(
    description='Generate fasta file with specific id format.')
parameters.add_argument('input', help='gb format file')
parameters.add_argument('-o', '--output', default='output.fasta',
                        help='output file')
parameters.print_help()
arg = parameters.parse_args()
handle = open(arg.output, 'w')
for sequence in SeqIO.parse(arg.input, 'genbank'):
    organism = sequence.annotations['organism'].replace(' ', '_')
    specimen = 'specimen_vourcher'
    isolate = 'isolate'
    gene = list()
    try:
        specimen = sequence.features[0].qualifiers['specimen_vourcher']
        isolate = sequence.features[0].qualifiers['isolate']
    except:
        pass
    for feature in sequence.features:
        if feature.type == 'gene' and 'gene' in feature.qualifiers:
            gene.append(feature.qualifiers['gene'][0].replace(' ', '_'))
        elif feature.type == 'misc_feature':
            try:
                misc_info = list(feature.qualifiers.values())[0]
            except:
                misc_info = ''
            print(misc_info)
            gene.append('_'.join(misc_info).replace(' ', '_'))
    gene = '-'.join(gene)
    handle.write('>{0}\n{1}\n'.format(
        '|'.join([organism, specimen, isolate, gene]), str(sequence.seq)))
