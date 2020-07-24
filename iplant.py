#!/usr/bin/python3

import re
from urllib.parse import quote
from urllib.request import urlopen
from sys import argv
from time import sleep


url = r'http://www.iplant.cn/info/'
pattern = re.compile(r'<title>(?P<name>.*)</title>', re.DOTALL)


def request(name):
    sleep(1)
    fullurl = url + quote(name)
    request = urlopen(fullurl)
    if request.status != 200:
        return name, ''
    raw = request.read()
    text = raw.decode('utf-8')
    search = re.search(pattern, text)
    if search.group() is not None:
        title = search.groupdict()['name'].strip()
    if title == '植物智':
        print(name, 'not found')
        return name, ''
    chinese, *latin_list = title.split(' ')
    latin = ' '.join(latin_list)
    return chinese, latin


def main():
    raw = open(argv[1], 'r', encoding='utf-8')
    out = open(argv[1]+'-out.txt', 'w', encoding='utf-8')
    miss = open(argv[1]+'-not_found.txt', 'w', encoding='utf-8')
    for line in raw:
        name = line.strip()
        chinese, latin = request(name)
        if latin != '':
            print(chinese, '#', latin)
            out.write(f'{chinese}#{latin}\n')
        else:
            miss.write(f'{chinese}\n')


if __name__ == '__main__':
    main()
