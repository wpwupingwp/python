#!/usr/bin/python3

genus_info = dict()
with open('./genus_info', 'r') as _:
    for line in _:
        genus, family, order, kind = line.split('\t')
        genus_info[genus] = [kind.strip(), order, family]

chinese_info = dict()
with open('./chinese_name.csv', 'r') as _:
    for line in _:
        chinese, genus, species, subspecies = line.split('\t')
        chinese_info[genus] = [genus, species, subspecies.strip()]

new = list()
update = list()
head = ''
with open('./DNABank-v5.0.csv', 'r') as _:
    head = _.readline()
    print(head)
    for line in _:
        info = line.split('\t')
        if info[10] == '' and info[11] == 'sp.' and info[5] != '':
            if info[5] in chinese_info:
                info[10], info[11], info[12] = chinese_info[info[5]]
                info[7], info[8], info[9] = genus_info[info[10]]
                update.append(info[0])
        new.append(info)
with open('new.csv', 'w') as out:
    out.write(head)
    for i in new:
        out.write('\t'.join(i))
with open('update_by_chinese.csv', 'w') as l:
    l.write('\n'.join(update))
