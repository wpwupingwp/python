﻿#!/usr/bin/python3

import argparse
import os
from Bio import SearchIO, SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline as nb
from glob import glob
from multiprocessing import cpu_count
from subprocess import run


def divide_barcode(barcode_len, skip):
    """Divide raw data via barcode.
    In this case, it searches primers in first 20bp sequence of reads, you may
    edit it.
    Before the search, it filters sequence accordting to the 5-2 repeat at the
    beginning.
    """
    # get barcode dict
    barcode = dict()
    with open(arg.barcode_file, 'r') as input_file:
        for line in input_file:
            if line.startswith('barcode') is True:
                continue
            line = line.split(sep=',')
            barcode[line[0]] = line[1]

    SEARCH_LEN = 20
    fastq_raw = SeqIO.parse(arg.input, 'fastq')
    total = 0
    half = barcode_len//2
    not_found = 0
    barcode_wrong = 0
    handle_miss = open('divide_barcode_miss.fastq', 'w')
    handle_fasta = open('divide_barcode.fasta', 'w')
    for record in fastq_raw:
        total += 1
        # ignore wrong barcode
        if str(record.seq[:half]) != str(record.seq[half:barcode_len]):
            barcode_wrong += 1
            continue
        record_barcode = [str(record.seq[:barcode_len]),
                          str(record.seq[:-(barcode_len + 1):-1])]
        if arg.strict:
            condition = (record_barcode[0] in barcode)
        else:
            condition = (record_barcode[0] in barcode and
                         record_barcode[1] in barcode)
        if condition:
            name = barcode[record_barcode[0]]
            output_file = 'out/{0}'.format(name)
            with open(output_file, 'a') as handle:
                SeqIO.write(record, handle, 'fastq')
            handle_fasta.write('>{0}\n{1}\n'.format(
                record.description,
                record.seq[skip:skip + SEARCH_LEN]))
        else:
            SeqIO.write(record, handle_miss, 'fastq')
            not_found += 1
    handle_miss.close()
    handle_fasta.close()
    return not_found, total


def get_primer_list():
    with open(arg.primer_file, 'r') as input_file:
        primer_raw = input_file.read().split(sep='\n')
    primer_raw.pop(0)
    primer_raw.pop(-1)
    primer_list = [i.split(sep=',') for i in primer_raw]
    return primer_list


def write_fasta(primer_list, primer_adapter):
    handle = open('primer.fasta', 'w')
    join_seq = 'N'*15
    gene_list = list()
    for index in range(0, len(primer_list) - 1, 2):
        left = primer_list[index][2][primer_adapter:]
        right = primer_list[index + 1][2][primer_adapter:]
        short_primer = ''.join([left, join_seq, right])
        name = primer_list[index][0]
        gene_list.append(name)
        handle.write('>{0}\n{1}\n'.format(name, short_primer))
    handle.close()
    return gene_list


def blast(query_file, db_file):
    """Use blastn-short for primers.
    """
    result = os.path.join(arg.output, 'BlastResult.xml')
    cmd = nb(
        num_threads=cpu_count(),
        query=query_file,
        db=db_file,
        task='blastn-short',
        evalue=arg.evalue,
        outfmt=5,
        out=result
    )
    stdout, stderr = cmd()
    return result


def parse_blast(blast_result):
    parse_result = list()
    blast_result = SearchIO.parse(blast_result, 'blast-xml')
    for record in blast_result:
        if len(record) == 0:
            continue
        else:
            tophit = record[0]
        query_info = '{0} {1}'.format(
            tophit[0][0].query_id,
            tophit[0][0].query_description)
        hit_info = tophit[0][0].hit.id
        parse_result.append([query_info, hit_info])
    parse_result = dict(parse_result)
    return parse_result


def step2(primer_adapter):
    """Step 2:
    BLAST fastq in first step against primer database.
    """
    primer_list = get_primer_list()
    gene_list = write_fasta(primer_list, primer_adapter)
    run('makeblastdb -in primer.fasta -out primer -dbtype nucl', shell=True)
    blast_result = parse_blast(blast('divide_barcode.fasta', 'primer'))
    return blast_result, gene_list


def step3(blast_result, file_list, gene_list):
    """Step 3:
    First, according BLAST result, split fastq files generated in
    divide_barcode, then assembly.
    """
    count_sample = {i: 0 for i in file_list}
    count_gene = {i: 0 for i in gene_list}
    for fastq_file in file_list:
        records = SeqIO.parse(fastq_file, 'fastq')
        for record in records:
            gene = record.description
            if gene in blast_result:
                count_sample[fastq_file] += 1
                count_gene[blast_result[gene]] += 1
                handle = open(
                    '{0}_{1}.fastq'.format(fastq_file, blast_result[gene]),
                    'a')
                SeqIO.write(record, handle, 'fastq')
    return count_sample, count_gene


def main():
    """
    Usage:
    python3 divide.py fastqFile barcodeFile primerFile
    Step 1, divide data by barcode. Step 2, divide data by primer via BLAST.
    Ensure that you have installed BLAST suite before.
    Make sure you don't miss the first line.
    Barcode file looks like this:
    ATACG,BOP00001
    Primer file looks like this:
    gene,primer,sequence
    rbcL,rbcLF,ATCGATCGATCGA
    rbcL,rbcLR,TACGTACGTACG
    Make sure you don't miss the first line.
    To get these two files, save your excel file as csv file.  Be carefull
    of the order of  each pair of primers.
    From left to right, there are:
    1. gene name
    2. primer name
    3. primer sequence
    4. forward/backward
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--barcode_length', default=10, type=int,
                        help='length of barcode')
    parser.add_argument('--primer_adapter', default=14, type=int,
                        help='length of primer_adapter, typical 14 for AFLP')
    parser.add_argument('-b', dest='barcode_file',
                        help='csv file containing barcode info')
    parser.add_argument('-p', dest='primer_file',
                        help='csv file containing primer info')
    parser.add_argument('-e', dest='evalue', default=1e-5, type=float,
                        help='evalue for BLAST')
    parser.add_argument('-s', '--strict', action='store_true',
                        help='''if set nostrict, it will only consider
                        barcode on the head; if not, consider head and tail''')
    parser.add_argument('-m', dest='mode', default='5-2',
                        help='''barcode mode, default value is 5-2, i.e.,
                        barcode with length 5 repeated twice''')
    parser.add_argument('input', help='input file, fastq format')
    parser.add_argument('-o', dest='output', default='out', help='output path')
    global arg
    arg = parser.parse_args()
    print(vars(arg))
    skip = arg.barcode_length + arg.primer_adapter
    if not os.path.exists(arg.output):
        os.mkdir(arg.output)
    miss_divide_barcode, total = divide_barcode(arg.barcode_length, skip)
    blast_result, gene_list = step2(arg.primer_adapter)
    file_list = glob(arg.output+'B*')
    count_sample, count_gene = step3(blast_result, file_list, gene_list)
    count_sample = list(count_sample.items())
    count_gene = list(count_gene.items())
    with open('count_sample', 'w') as handle:
        for i in count_sample:
            handle.write('{0} {1} \n'.format(i[0], i[1]))
    with open('count_gene', 'w') as handle:
        for i in count_gene:
            handle.write('{0} {1} \n'.format(i[0], i[1]))

if __name__ == '__main__':
    main()
