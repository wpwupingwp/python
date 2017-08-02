#!/usr/bin/python3

import os
from urllib import request


def down():
    URL = r'http://www.onekp.com/public_data.html'

    raw = request.urlopen(URL)
    if raw.code != '200':
        raise Exception('Cannot open {}. Quit now.'.format(URL)
    with open('public_data.html', 'w') as output:
        output.write(raw.read())



info = list()
with open(argv[1], 'r') as raw:
    for line in raw:
        if line.startswith('<table'):
            break
    for line in raw:
        if line.strip().startswith('<tr>'):
            record = list()
            continue
        record.append(line.strip())
        if line.strip().startswith('</tr>'):
            info.append(record)
            continue

