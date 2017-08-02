#!/usr/bin/python3

import os
from urllib import request


def down(url, html):
    raw = request.urlopen(url)
    if raw.code != 200:
        raise Exception('Cannot open {}. Quit now.'.format(url))
    with open(html, 'w') as output:
        output.write(raw.read().decode('utf-8'))


def parse(html):
    info = list()
    record = list()
    handle = open(html, 'r')
    for line in handle:
        if line.startswith('<table'):
            break
    for line in handle:
        if line.strip().startswith('<tr>'):
            # record.clear()
            record = list()
            continue
        record.append(line.strip())
        if line.strip().startswith('</tr>'):
            info.append(record)
            continue
        if line.strip().startswith('</table>'):
            break

    handle.close()
    print(info)


def main():
    url = 'http://www.onekp.com/public_data.html'
    html = 'public.html'

    if not os.path.exists(html):
        down(url, html)
    parse(html)
    print('Done')


if __name__ == '__main__':
    main()
