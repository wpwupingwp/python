#!/usr/bin/python3

import requests

url = 'http://services.tropicos.org/Name/{}'
with open('apikey', 'r') as _:
    apikey = _.read().strip()
output = open('info.json', 'w')
with open('./list.csv', 'r') as _:
    for index, line in enumerate(_):
        nameid = line.split('\t')[0]
        params = {'apikey': apikey, 'format': 'json'}
        a = requests.get(url.format(nameid), params=params)
        info = a.text
        output.write(info)
        output.write('\n')
        print(index+1)
