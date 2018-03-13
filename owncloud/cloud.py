#!/usr/bin/python3

from lxml import etree
from requests import request

with open('key', 'r') as _:
    login = _.read().strip().split(' ')
    login = tuple(login)
a = request('PROPFIND',
            'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags',
            auth=login, data=open('./get_tag_detail.xml', 'rb'))
b = etree.fromstring(a.text)
nsmap = b.nsmap
c = b.findall('*//d:prop', namespaces=nsmap)
tag = dict()
for i in c:
    i_id = i.find('oc:id', namespaces=nsmap)
    i_name = i.find('oc:display-name', namespaces=nsmap)
    tag[i_id.text] = i_name.text
#print(b.text)
print(*tag.items())
