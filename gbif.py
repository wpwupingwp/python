#!/usr/bin/python3

import json
from urllib.request import urlopen
from sys import argv
from time import sleep

url = r'https://api.gbif.org/v1/species/'


def request(name, limit=3):
    sleep(0.1)
    fullurl = f'{url}?name={name}&limit={limit}'
    request = urlopen(fullurl)
    if request.status != 200:
        return name, ''
    raw = request.read()
    # text = raw.decode('utf-8')
    json_dict = json.load(raw)
    if len(json_dict['results']) == 0:
        return name, ''
    family = ''
    gbif_taxon_id = ''
    dan_or_shuang = ''
    for result in json_dict['results']:
        if result['synonym']:
            continue
        if 'class' not in result:
            continue
        family = result['family']
        gbif_taxon_id = result['taxonID']
        dan_or_shuang = result['class']
        break
    print(name, family, gbif_taxon_id, dan_or_shuang)
    return name, family, gbif_taxon_id, dan_or_shuang


def main():
    raw = open(argv[1], 'r', encoding='utf-8')
    out = open(argv[1]+'-out.txt', 'w', encoding='utf-8')
    miss = open(argv[1]+'-not_found.txt', 'w', encoding='utf-8')
    for line in raw:
        name = line.strip()
        chinese, latin = request(name)
        if latin == '':
            miss.write(f'{chinese}\n')
        out.write(f'{chinese}#{latin}\n')


if __name__ == '__main__':
    main()
