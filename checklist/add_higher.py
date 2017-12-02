#!/usr/bin/python3

# NCBI taxonomy have complex prefix in high rank, so here only use
# there three "phylum"
kinds = {'Acrogymnospermae', 'Lycopodiopsida', 'Mesangiospermae',
         'Polypodiopsida', 'basal Magnoliophyta'}
genus_list = set()
with open('./list.csv', 'r') as _:
    for line in _:
        genus_list.add(line.split('\t')[1])

result = list()
with open('./genus_info', 'r') as raw:
    for line in raw:
        info = line.split('\t')
        genus = info[0]
        # if genus not in genus_list:
        #     continue
        family = ''
        order = ''
        kind = ''
        for item in info:
            if item.endswith('aceae'):
                family = item
            elif item.endswith('ales'):
                order = item
            elif item in kinds:
                kind = item
                break
        result.append([genus, family, order, kind])
with open('result.csv', 'w') as out:
    for i in result:
        out.write('\t'.join(i)+'\n')
