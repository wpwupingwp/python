#!/usr/bin/python3

from os.path import exists
from lxml.html import parse


def main():
    url = 'http://www.onekp.com/public_data.html'
    html = 'public.html'
    handle = open('result.tsv', 'w')

    if not exists(html):
        raw = parse(url)
    else:
        raw = parse(html)
    # /html/body/table/tr/td/self|b|a.href
    all_tr = raw.xpath('//tr')
    for tr in all_tr:
        all_td = tr.findall('td')
        for td in all_td:
            # some <td> have descdents, get a.href
            for i in td.iter():
                if i.tag == 'a':
                    handle.write(i.attrib['href'])
                    break
                elif i.tag == 'td':
                    handle.write(i.text_content()+' ')
                else:
                    pass
            handle.write('\t')
        handle.write('\n')
    handle.close()
    print('Done')


if __name__ == '__main__':
    main()
