#!/usr/bin/python3

import argparse
import os
import re

import numpy as np
import primer3
from collections import defaultdict
from multiprocessing import cpu_count
from timeit import default_timer as timer
from subprocess import run

from Bio import SearchIO, SeqIO
from Bio.Data.IUPACData import ambiguous_dna_values
from Bio.Blast.Applications import NcbiblastnCommandline as nb


def get_ambiguous_dict():
    data = ambiguous_dna_values
    data = dict(zip(data.values(), data.keys()))
    # 2:{'AC': ['M',}
    data_with_len = defaultdict(lambda: dict())
    for key in data:
        data_with_len[len(key)][key] = data[key]
    return data_with_len


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


def convert(old):
    # order 'F' is a bit faster than 'C'
    # name = np.array([[i[0]] for i in old], dtype=np.bytes_)
    # seq = np.array([list(i[1]) for i in old], dtype=np.bytes_)
    # new = np.hstack((name, seq))
    new = np.array([list(i[1]) for i in old], dtype=np.bytes_, order='F')
    rows, columns = new.shape
    return new, rows, columns


def count(alignment, rows, columns):
    # skip sequence id column
    data = [[rows, columns]]
    for index in range(columns):
        column = alignment[:, [index]]
        unique, counts = np.unique(column, return_counts=True)
        count_dict = {b'A': 0, b'T': 0, b'C': 0, b'G': 0, b'N': 0,
                      b'-': 0, b'?': 0}
        count_dict.update(dict(zip(unique, counts)))
        a = count_dict[b'A']
        t = count_dict[b'T']
        c = count_dict[b'C']
        g = count_dict[b'G']
        n = count_dict[b'N']
        gap = count_dict[b'-']
        question = count_dict[b'?']
        # is it necessary to count 'N' '-' and '?' ?
        other = rows - a - t - c - g - n - question - gap
        data.append([a, t, c, g, n, question, gap, other])
    # make sure rows and columns does not mixed
    assert len(data) == columns + 1
    return data


def find_most(data, cutoff, gap_cutoff):
    # to be continue
    # directly use np.unique result
    most = [['location', 'base', 'count']]
    rows, columns = data[0]
    data = data[1:]
    gap_cutoff = rows * gap_cutoff
    cutoff = rows * cutoff
    ambiguous_dict = get_ambiguous_dict()

    def run():
        for location, column in enumerate(data, 1):
            finish = False
            value = dict(zip(list('ATCGN?-X'), column))
            base = 'N'

            sum_gap = sum([value['?'], value['-'], value['X']])
            if sum_gap >= gap_cutoff:
                base = '-'
                count = sum_gap
                yield [location, base, count]
                continue
            # 1 2 3 4
            for length in ambiguous_dict:
                if finish:
                    break
                for key in ambiguous_dict[length]:
                    if finish:
                        break
                    count = 0
                    for letter in list(key):
                        if finish:
                            break
                        count += value[letter]
                        if count >= cutoff:
                            base = ambiguous_dict[length][key]
                            finish = True
                            yield [location, base, count]
    for i in run():
        most.append(i)
    return most[1:]


def find_continuous(most):
    continuous = list()
    fragment = list()
    most = [i for i in most if i[1] not in ('N', '-')]
    for index, value in enumerate(most):
        fragment.append(value)
        location, *_ = value
        try:
            location_next, *_ = most[index+1]
        except:
            fragment.append(value)
# to be continue
            break
        step = location_next - location
        if step > 1:
            continuous.append(fragment)
            fragment = list()
    return continuous


def find_primer(continuous, most, min_len, max_len, ambiguous_base_n):
    poly = re.compile(r'([ATCG])\1\1\1\1')
    ambiguous_base = re.compile(r'[^ATCG]')
    tandem = re.compile(r'([ATCG]{2})\1\1\1\1')

    def is_good_primer(primer):
        # ref1. http://www.premierbiosoft.com/tech_notes/PCR_Primer_Design.html
        seq = ''.join([i[1] for i in primer])
        if re.search(poly, seq) is not None:
            return False, 0, 'Poly(NNNNN) structure found'
        if re.search(tandem, seq) is not None:
            return False, 0, 'Tandom(NN*5) exist'
            # no more 3 ambiguous base
        if len(re.findall(ambiguous_base, seq)) >= ambiguous_base_n:
            return False, 0, 'More than 3 ambiguous base'

# primer3.setGlobals seems have no effect on calcTm, so I have to replace all
# ambiguous base to A to get an approximate value. Othervise calcTm() will
# generate -99999 if there is ambiguous base.
        pure_seq = re.sub(ambiguous_base, 'A', seq)
        tm = primer3.calcTm(pure_seq)
        hairpin_tm = primer3.calcHairpinTm(pure_seq)
        homodimer_tm = primer3.calcHomodimerTm(pure_seq)
        if max(tm, hairpin_tm, homodimer_tm) != tm:
            return False, 0, 'Hairpin or homodimer found'
        return True, tm, 'Ok'

    primer = list()
    continuous = [i for i in continuous if len(i) >= min_len]
    for fragment in continuous:
        len_fragment = len(fragment)
        for start in range(len_fragment-max_len):
            for p_len in range(min_len, max_len):
                seq = fragment[start:(start+p_len)]
                good_primer, tm, detail = is_good_primer(seq)
                if good_primer:
                    primer.append([seq, tm])
                else:
                    continue
    primer.sort(key=lambda x: x[1], reverse=True)
    return primer


def parse(blast_result_file):
    sep = '~'*80
    blast_result = SearchIO.parse(blast_result_file, 'blast-xml')
    for query in blast_result:
        if len(query) == 0:
            continue
        # Blast Result
        #   |_query
        #       |_hit
        #           |_hsp
        hits = list(query)
        hits.sort(key=lambda x: x[0].bitscore_raw, reverse=True)
        best_hsp = hits[0][0]
        for hsp in hits[1:]:
            if hsp[0].bitscore_raw == best_hsp.bitscore_raw:
                print('Same BLAST score:\n{}\n{}\n{}'.format(best_hsp, hsp[0],
                                                             sep))
                yield hsp[0]
            else:
                break
        yield best_hsp


def validate(candidate_file, input_file, n_seqs, min_len, min_covrage,
             max_mismatch):
    # remove gap in old alignment file
    no_gap = 'validate.fasta'
    with open(no_gap, 'w') as new, open(input_file, 'r') as old:
        for line in old:
            if line.startswith('>'):
                new.write(line)
            else:
                new.write(line.replace('-', ''))

    # build blast db
    candidate_fasta = 'primer_candidate.fasta'
    SeqIO.convert(candidate_file, 'fastq', candidate_fasta, 'fasta')
    run('makeblastdb -in {} -dbtype nucl'.format(no_gap), shell=True)
    # blast
    blast_result_file = 'BlastResult.xml'
    cmd = nb(num_threads=cpu_count(),
             query=candidate_fasta,
             db=no_gap,
             task='blastn',
             evalue=1e-5,
             max_hsps=1,
             max_target_seqs=n_seqs,
             outfmt=5,
             out=blast_result_file)
    stdout, stderr = cmd()
    # parse
    min_bitscore_raw = min_len - max_mismatch
    blast_result = [['ID', 'Hits', 'Sum_Bitscore_raw', 'Seq'], ]
    blast_result.append(['All', n_seqs, min_len, 'N'*min_len])
    for query in SearchIO.parse(blast_result_file, 'blast-xml'):
        if len(query) == 0:
            blast_result.append([query.id, 0, 0])
            continue
        seq = str(query[0][0].query.seq)
        sum_bitscore_raw = 0
        good_hits = 0
        for hit in query:
            hsp_bitscore_raw = hit[0].bitscore_raw
            if hsp_bitscore_raw >= min_bitscore_raw:
                sum_bitscore_raw += hsp_bitscore_raw
                good_hits += 1
        blast_result.append([query.id, good_hits, sum_bitscore_raw, seq])
    # validate
    validate_result = [blast_result[:2], ]
    for record in blast_result:
        if record[1] / n_seqs >= min_covrage:
            validate_result.append(record)
    validate_result.sort(key=lambda x: x[2])
    return validate_result


def write_fastq(data, rows, output, cutoff, name):
    # https://en.wikipedia.org/wiki/FASTQ_format
    quality = ('''!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'''
               '''[\]^_`abcdefghijklmnopqrstuvwxyz{|}~''')
    l = len(quality)
    output = open(output, 'w')

    data.sort(key=lambda x: int(x[-1]), reverse=True)
    for item, tm in data:
        start = item[0][0]
        end = item[-1][0]
        length = end - start + 1
        seq = ''.join([i[1] for i in item])
        qual = [round((i[2]/rows)*l)-1 for i in item]
        qual = [quality[int(i)] for i in qual]
        output.write('@{}-{}-{}-{}bp-{:.2f}°C-{:.0%}\n'.format(
            name, start, end, length, tm, cutoff))
        output.write(seq+'\n')
        output.write('+\n')
        output.write(''.join(qual)+'\n')
    return output


def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('input', help='input alignment file')
    arg.add_argument('-a', '--ambiguous_base_n', type=int, default=2,
                     help='number of ambiguous bases')
    arg.add_argument('-c', '--cutoff', type=float, default=1.0,
                     help='minium percent to keep')
    arg.add_argument('-g', '--gap_cutoff', type=float, default=0.5,
                     help='maximum percent for gap to cutoff')
    arg.add_argument('-n', '--name', help='name prefix')
    arg.add_argument('-l', '--length', type=str, default='24-25',
                     help='primer length range')
    arg.add_argument('-m', '--mismatch', type=int, default=2,
                     help='maximum mismatch bases in primer')
    # arg.print_help()
    return arg.parse_args()


def main():
    start = timer()
    arg = parse_args()
    if arg.name is None:
        arg.name = os.path.basename(arg.input)
        arg.name = arg.name.split('.')[0]
    min_len, max_len = arg.length.split('-')
    min_len = int(min_len)
    max_len = int(max_len)

    raw_alignment = read(arg.input)
    new, rows, columns = convert(raw_alignment)
    count_data = count(new, rows, columns)
    most = find_most(count_data, arg.cutoff, arg.gap_cutoff)
    # write consensus
    write_fastq([[most, 0]], rows, arg.name+'.consensus.fastq', arg.cutoff,
                arg.name)
    continuous = find_continuous(most)
    primer_candidate = find_primer(continuous, most, min_len, max_len,
                                   arg.ambiguous_base_n)
    candidate_file = write_fastq(
        primer_candidate, rows, arg.name+'.candidate.fastq',
        arg.cutoff, arg.name)
    primer = validate(candidate_file, arg.input, rows, min_len, arg.cutoff,
                      arg.mismatch)
    print('Found {} primers.'.format(len(primer)))
    write_fastq(primer, rows, arg.name+'.primer.fastq', arg.cutoff, arg.name)
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
