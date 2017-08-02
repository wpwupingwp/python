#!/usr/bin/python3

from os.path import exists
from lxml.html import parse


def main():
    url = 'http://www.onekp.com/public_data.html'
    html = 'public.html'

    if not exists(html):
        raw = parse(url)
    else:
        raw = parse(html)
    # /html/body/table/tr/td/self|b|a.href
    table = raw.find('/body/table')
    for tr in table:
        td = tr.findall('td')
        for i in td:
            # some <td> have descdents, get a.href
            for j in i.iter():
                if j.tag == 'a':
                    print('a', j.attrib['href'])
                elif j.tag == 'td':
                    print('td', j.text_content())
            print()
        print('-'*80)

    print('Done')


if __name__ == '__main__':
    main()
