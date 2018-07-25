from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from timeit import default_timer as timer
from sys import argv


def main():
    start = timer()
    print('Usage: python3 trim.py filename "from:to"')
    filename, from_to = argv[1:3]
    head, tail = from_to.split(':')
    head = int(head)
    if head > 0:
        head -= 1
    tail = int(tail)
    print(head, tail)
    with open('{}.new.fasta'.format(filename), 'w') as output:
        for record in SeqIO.parse(filename, 'fasta'):
            new = record[0:head] + record[tail:]
            SeqIO.write(new, output, 'fasta')
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
