#!/usr/bin/python3

from lxml import etree
from requests import request
from requests.utils import quote, unquote
from pathlib import Path
import json


def get_tag_info(url, user, passwd):
    r = request('PROPFIND', url, auth=(user, passwd),
                data=open('./propfind-tagid.xml', 'rb'))
    xml = etree.fromstring(r.content)
    nsmap = xml.nsmap
    response = xml.findall('d:response', namespaces=nsmap)
    # name:id
    tag_dict = dict()
    href = list()
    for i in response:
        i_id = i.find('*//oc:id', namespaces=nsmap)
        i_name = i.find('*//oc:display-name', namespaces=nsmap)
        tag_dict[i_name.text] = i_id.text
        href.append(i.find('d:href', namespaces=nsmap).text)
    return tag_dict, href


def get_tag_id(fileid, url, user, passwd):
    url = url + fileid
    _, href = get_tag_info(url, user, passwd)
    print(*href, end='\n')


def create_tag(tag_name, url, user, passwd):
    d = {'name': tag_name,
         'userVisible': True,
         'userAssignable': True}
    headers = {'content-type': 'application/json'}
    r = request('POST', url, auth=(user, passwd), data=json.dumps(d),
                headers=headers)


def delete_tag(tag_id, url, auth):
    r = request('DELETE', url+'/{}'.format(tag_id), auth=auth)


def get_fileid(path, url, user, passwd):
    r = request('PROPFIND', url=url+'/{}/{}'.format(user, quote(path)),
                auth=(user, passwd), data=open('./propfind-fileid.xml', 'rb'),
                headers={'Depth': '1'})
    xml = etree.fromstring(r.text)
    nsmap = xml.nsmap
    response = xml.findall('d:response', namespaces=nsmap)
    # filename:id
    file_dict = dict()
    for i in response:
        fullname = i.find('d:href', namespaces=nsmap).text
        filename = Path(fullname).name.__str__()
        #fileid = i.find('d:propstat/d:prop/oc:fileid', namespaces=nsmap)
        fileid = i.find('*//oc:fileid', namespaces=nsmap).text
        file_dict[filename] = fileid
    return file_dict





def main():
    tag_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags'
    list_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/files'
    file_tag_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags-relations/files/'
    folder = '01___薄荷曲库___01'
    with open('key', 'r') as _:
        raw = _.read().strip().split(' ')
        user, passwd = raw
    tag_dict = get_tag_info(tag_url, user, passwd)
    filename_id_dict = get_fileid(folder, list_url, user, passwd)
    get_tag_id(i, file_tag_url, user, passwd)
    # tag_id = input('Enter tag id to list file:')
    # list_file_by_tag(tag_id, list_url, auth)
    # tag_name = input('Enter new tag name:')
    # create_tag(tag_url, auth, tag_name)
    # tag_name = input('Enter tag name you want to delete:')
    # tag_id = tag_dict[tag_name]
    # delete_tag(tag_url, auth, tag_id)


if __name__ == '__main__':
    main()
