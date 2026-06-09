from pathlib import Path
import argparse

from Bio import SeqIO

def stats(data: list):
    mean = sum(data) / len(data)
    differences = [(x - mean) for x in data]
    std_dev = (sum([diff ** 2 for diff in differences]) / len(data)) ** 0.5
    z_scores = [(x - mean) / std_dev for x in data]
    min_len = min(data)
    max_len = max(data)
    s = sorted(data)
    middle = s[len(s)//2]
    return min_len, max_len, mean, middle, std_dev, z_scores


def parse_arg():
    arg = argparse.ArgumentParser(usage=main.__doc__)
    arg.add_argument('fasta', help='fasta filename')
    arg.add_argument('z_score_limit', default=5, type=float, help='zscore limit')
    arg.add_argument('-do_filter', action='store_true', help='output filtered fasta')
    return arg.parse_args()


def main():
    '''Usage: python3 filter_length.py filename zscore_limit do_filter_or_not'''
    arg = parse_arg()
    arg.fasta = Path(arg.fasta).resolve()
    new_fasta = arg.fasta.with_suffix('.new.fasta')
    report = arg.fasta.with_suffix('.report')

    len_name = list()
    good_index = set()
    for i in SeqIO.parse(arg.fasta, 'fasta'):
        length = len(i)
        name = i.id
        len_name.append([length, name])
    min_len, max_len, mean, middle, std_dev, z_scores = stats([i[0] for i in len_name])
    bad = 0
    report_h = open(report, 'w')
    report_h.write('Zscore\tLength\tName\n')
    for i, z in enumerate(z_scores):
        if abs(z) > arg.z_score_limit:
            bad +=  1
            line = f'{z:>6.2f}\t{len_name[i][0]:>5}\t{len_name[i][1]}\n'
            print(line, end='')
            report_h.write(line)
        else:
            good_index.add(i)
    overall = f'#{min_len=} {max_len=} {mean=:.2f} {std_dev=:.2f} {middle=} z_score_limit={arg.z_score_limit} {bad=} n={len(len_name)}'
    print(overall)
    report_h.write(overall)
    report_h.close()
    if arg.do_filter:
        out_h = open(new_fasta, 'w')
        for i, r in enumerate(SeqIO.parse(arg.fasta, 'fasta')):
            if i in good_index:
                SeqIO.write(r, out_h, 'fasta')
        out_h.close()


main()
