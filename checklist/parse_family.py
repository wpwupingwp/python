#!/usr/bin/python3

from glob import glob
from lxml import html
import re

files = glob("*.html")
output = open("list.csv", "w", encoding="utf-8")
pattern = r"\d+"
for page in files:
    # if directly use html.parse(file), encode error occurs
    with open(page, "r") as raw:
        raw = raw.read()
    data = html.fromstring(raw)
    table = data.xpath('//*[@id="dataTable"]/tbody')[0]
    all_a = table.findall("*//a")
    for a in all_a:
        text = a.text_content()
        name = text
        find = re.search(pattern, a.attrib["href"])
        if find is not None:
            nameid = find.group()
        # name = text.strip()
        name_list = name.split(" ")
        family, author, *etc = name_list
        if family == "×":
            family = "".join([family, author])
            author = "".join(etc)
        else:
            author = " ".join([author, *etc])
        output.write("{}\t{}\t{}\n".format(nameid, family, author))
