#!/usr/bin/python3

import re
from urllib.parse import quote
from urllib.request import urlopen
from sys import argv
from time import sleep
try:
    from lxml import etree
except ImportError:
    raise SystemExit('Cannot find lxml. Run "pip install --user lxml"')


url = r'http://www.iplant.cn/info/'
# pattern = re.compile(r'<title>(?P<name>.*)</title>', re.DOTALL)
pattern = re.compile(r'[A-Za-z ]+')

def request(name: str) ->str:
    sleep(0.5)
    fullurl = url + quote(name)
    request = urlopen(fullurl)
    if request.status != 200:
        return ''
    else:
        raw = request.read()
        text = raw.decode('utf-8')
        return text


def get_text(element: 'Element') ->str:
    if len(element) == 0:
        return ''
    else:
        text = element[0].text
        if text is None:
            text = ''
        return text


def parse(text: str):
    #a = html.document_fromstring(raw)
    a = etree.HTML(text)
    cname_path = a.xpath('//*[@class="infocname"]')
    cname = get_text(cname_path)
    name_path = a.xpath('//*[@id="sptitlel"]')
    name = get_text(name_path)
    change_path = a.xpath('//*[@class="infomore"]/*[@class="spantxt"]/a')
    change_name_raw = get_text(change_path)
    _ = re.search(pattern, change_name_raw)
    if _ is None:
        change_name = ''
    else:
        change_name = _.group()
    print(cname, name, change_name)
    return cname, name, change_name


def old():
    # deprecated
    name = ''
    text = ''
    title = ''
    search = re.search(pattern, text)
    if search.group() is not None:
        title = search.groupdict()['name'].strip()
    if title == '植物智':
        print('!', name, 'NOT FOUND')
        return name, ''
    chinese, *latin_list = title.split(' ')
    latin = ' '.join(latin_list)
    print(chinese, latin)
    return chinese, latin


def main():
    raw = open(argv[1], 'r', encoding='utf-8')
    out = open(argv[1]+'-out.txt', 'w', encoding='utf-8')
    out.write('Raw_name,Name,Chinese,Changed_Name\n')
    for line in raw:
        raw_name = line.strip()
        text = request(raw_name)
        if text == '':
            cname, name, change_name = 'NOT_FOUND', raw_name, 'NOT_FOUND'
        else:
            cname, name, change_name = parse(text)
        out.write(f'{raw_name},{name},{cname},{change_name}\n')


if __name__ == '__main__':
    main()
