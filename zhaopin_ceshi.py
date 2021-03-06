from Bio import SeqIO
from glob import glob
from hashlib import sha256
from random import shuffle

files = glob('*.fasta')
old_new = []
to_change = []
ratio = 0.20
for i in files:
    data = []
    raw = SeqIO.parse(i, 'fasta')
    count = 0
    for j in raw:
        count += 1
        gene = j.name.split('|')[0]
        new = sha256(j.name.encode('ascii')).hexdigest()
        assert j.name == j.description
        old_new.append([gene, j.name, new])
        j.id = new
        j.name = new
        j.description = new
        data.append(j)
    for k in range(0, int(count*ratio)):
        to_change.append(data.pop())
    SeqIO.write(data, i+'.clean', 'fasta')
    print(i, count)
shuffle(to_change)
len_tochange = len(to_change) // 5
print('to change', len(to_change))
for fasta in glob('*.clean'):
    clean = list(SeqIO.parse(fasta, 'fasta'))
    dirty = []
    for m in range(0, len_tochange):
        dirty.append(to_change.pop())
    print(fasta, 'clean', len(clean), 'dirty', len(dirty))
    clean.extend(dirty)
    shuffle(clean)
    with open(fasta+'.mix', 'w') as out:
        SeqIO.write(clean, out, 'fasta')
with open('answer.txt', 'w') as out:
    out.write('gene,old,new\n')
    for line in old_new:
        out.write(','.join(line)+'\n')
