#!/usr/bin/python3


from sys import argv
from urllib import request
from urllib.error import URLError

print('URL list looks like\nname\taddress\n')
url_list = list()
fail = open('fail.log', 'w')
with open(argv[1], 'r') as raw:
    for line in raw:
        line = line.strip()
        # use default splitter
        url_list.append(line.split())

for name, *_, url in url_list:
    try:
        get = request.urlopen(url)
    except URLError:
        fail.write('{}\t{}\n'.format(name, url))
        continue

    if get.code != 200:
        fail.write('{}\t{}\n'.format(name, url))
        continue
    with open(name, 'wb') as output:
        output.write(get.read())

fail.close()
print('Done.')
