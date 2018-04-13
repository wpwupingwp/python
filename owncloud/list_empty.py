#!/usr/bin/python3

from lxml import etree
from requests import request
from requests.utils import quote, unquote
from pathlib import Path


def get_fileid(path, url, user, passwd):
    r = request('PROPFIND', url=url+'/{}/{}'.format(user, quote(path)),
                auth=(user, passwd), data=open('./propfind-fileid.xml', 'rb'),
                headers={'Depth': '1'})
    xml = etree.fromstring(r.content)
    nsmap = xml.nsmap
    response = xml.findall('d:response', namespaces=nsmap)
    # filename:id
    file_dict = dict()
    for i in response:
        fullname = i.find('d:href', namespaces=nsmap).text
        filename = Path(fullname).name.__str__()
        #fileid = i.find('d:propstat/d:prop/oc:fileid', namespaces=nsmap)
        fileid = i.find('*//oc:fileid', namespaces=nsmap).text
        file_dict[unquote(filename)] = fileid
    return file_dict


def main():
    list_url = 'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/files'
    folder = '01___薄荷曲库___01'
    with open('./key', 'r') as _:
        a = _.readline()
        a = a.strip()
        a = a.split(' ')
        user, passwd = a
    folder_list = get_fileid(folder, list_url, user, passwd)
    for i in folder_list:
        children = get_fileid(folder+'/'+i, list_url, user, passwd)
        print(i, len(children), *children.keys())


if __name__ == '__main__':
    main()
