#!/usr/bin/python3

from glob import glob
from lxml import html

files = glob('*.html')
output = open('list.csv', 'w', encoding='utf-8')
for page in files:
    # if directly use html.parse(file), encode error occurs
    with open(page, 'r') as raw:
        raw = raw.read()
    data = html.fromstring(raw)
    table = data.xpath('//*[@id="dataTable"]/tbody')[0]
    all_a = table.findall('*//a')
    for a in all_a:
        text = a.text_content()
        name = text
        print(name)
        # name = text.strip()
        name_list = name.split(' ')
        genus, species, *ssp = name_list
        ssp = ' ' .join(ssp)
        output.write('{}\t{}\t{}\n'.format(genus, species, ssp))
