#!/usr/bin/python3

import json

handle = open('./info.json', 'r')
output = open('info.csv', 'w')
for line in handle:
    info = json.loads(line)
    keys = info.keys()
    keys = [str(i) for i in keys]
    values = [str(info[i]) for i in keys]
    output.write('\t'.join(keys))
    output.write('\n')
    output.write('\t'.join(values))
    output.write('\n')
