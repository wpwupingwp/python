#!/usr/bin/python3

import json
import logging
import re
from pathlib import Path
from sys import argv
from time import sleep
from urllib.parse import quote
from urllib.request import urlopen
try:
    from lxml import etree
except ImportError:
    raise SystemExit('Cannot find lxml. Run "pip install --user lxml"')

FMT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%H:%M:%S'
LOG_FMT = logging.Formatter(fmt=FMT, datefmt=DATEFMT)
logging.basicConfig(format=FMT, datefmt=DATEFMT, level=logging.INFO)
log = logging.getLogger('iplant')

url = r'http://www.iplant.cn/info/'
#pattern = re.compile(r'[A-Za-z \.]+')
pattern = re.compile(r'[\u4e00-\u9fa5]+\s(\S.+)')
sleep_time = 0.5
cache_file = Path().cwd() / 'iplant_cache.json'


def read_cache() -> dict:
    if cache_file.exists():
        log.info('Found cache file. Use cache to reduce running time.')
        log.info('If you do not want to use it, delete it before running.')
        with open(cache_file, 'r', encoding='utf-8') as _:
            try:
                cache = json.load(_)
            except json.decoder.JSONDecodeError:
                log.error('Bad cache, ignore.')
                cache = dict()
    else:
        cache = dict()
    return cache


def write_cache(cache: dict):
    log.info(f'Write cache into {cache_file}')
    with open(cache_file, 'w', encoding='utf-8') as out:
        json.dump(cache, out)
    return


def request(name: str) ->str:
    sleep(sleep_time)
    fullurl = url + quote(name)
    try:
        request = urlopen(fullurl)
    except Exception:
        log.error('Failed to open website.')
        log.info(f'Stop at {name}')
        raise SystemExit(-1)
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


def parse(text: str, raw_name: str):
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
        change_name = _.group(1)
    print('change',change_name, change_name_raw)
    log.info(f'{raw_name}: {name}, {cname}, {change_name}')
    return cname, name, change_name


def main():
    log.info('Usage: python3 iplant.py list_file')
    raw = open(argv[1], 'r', encoding='utf-8')
    out = open(argv[1]+'-out.txt', 'w', encoding='utf-8')
    cache = read_cache()
    out.write('Raw_name,Name,Chinese,Changed_Name\n')
    log.info('Query: Name, Chinese Name, Changed Name')
    for line in raw:
        raw_name = line.strip()
        if raw_name in cache:
            cname, name, change_name = cache[raw_name]
            log.info(f'Found in cache: '
                     f'{raw_name}, {name}, {cname}, {change_name}')
        else:
            text = request(raw_name)
            if text == '':
                cname, name, change_name = 'NOT_FOUND', raw_name, 'NOT_FOUND'
            else:
                cname, name, change_name = parse(text, raw_name)
            cache[raw_name] = [cname, name, change_name]
        out.write(f'{raw_name},{name},{cname},{change_name}\n')
    write_cache(cache)
    log.info('Done.')


if __name__ == '__main__':
    main()
