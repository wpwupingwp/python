#!/usr/bin/python3

from lxml import etree
from requests import request

with open('key', 'r') as _:
    login = _.read().strip().split(' ')
    login = tuple(login)
get_tag_detal = """
<?xml version="1.0" encoding="utf-8" ?>
<a:propfind xmlns:a="DAV:" xmlns:oc="http://owncloud.org/ns">
  <a:prop>
    <!-- Retrieve the display-name, user-visible, and user-assignable properties -->
    <oc:display-name/>
    <oc:user-visible/>
    <oc:user-assignable/>
    <oc:id/>
  </a:prop>
</a:propfind>
"""
a = request('PROPFIND',
            'https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags',
            auth=login)
b = etree.fromstring(a.text)
print(b)
