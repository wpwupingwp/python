#!/usr/bin/python3

from lxml import etree
from requests import request
import json


def get_tag_list(url, auth):
    r = request('PROPFIND', url, auth=auth,
                data=open('./get_tag_detail.xml', 'rb'))
    b = etree.fromstring(r.text)
    nsmap = b.nsmap
    c = b.findall('*//d:prop', namespaces=nsmap)
    # name:id
    tag_dict = dict()
    for i in c:
        i_id = i.find('oc:id', namespaces=nsmap)
        i_name = i.find('oc:display-name', namespaces=nsmap)
        tag_dict[i_name.text] = i_id.text
    return tag_dict


def create_tag(url, auth, tag_name):
    d = {'name': tag_name,
         'userVisible': True,
         'userAssignable': True}
    headers = {'content-type': 'application/json'}
    r = request('POST', url, auth=auth, data=json.dumps(d),
                headers=headers)
    print(r.text)


def delete_tag(url, auth, tag_id):
    r = request('DELETE', url+'/{}'.format(tag_id), auth=auth)
    print(r.text)


def main():
    tag_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags'
    list_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/'
    with open('key', 'r') as _:
        raw = _.read().strip().split(' ')
        auth = tuple(raw)
    tag_dict = get_tag_list(tag_url, auth)
    tag_name = input('Enter new tag name:')
    create_tag(tag_url, auth, tag_name)
    tag_dict = get_tag_list(tag_url, auth)
    for i in tag_dict.items():
        print(*i)
    tag_name = input('Enter tag name you want to delete:')
    tag_id = tag_dict[tag_name]
    delete_tag(tag_url, auth, tag_id)
    tag_dict = get_tag_list(tag_url, auth)
    for i in tag_dict.items():
        print(*i)


if __name__ == '__main__':
    main()
