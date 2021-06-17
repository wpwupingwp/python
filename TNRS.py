#!/usr/bin/python3

from sys import argv
from pathlib import Path
import json
import csv

import requests
import certifi
print('Note: certifi should be the newest version')



def read_csv(old: Path) -> set:
    """
    csv should only contain one column
    """
    data = set()
    n = 0
    with open(old, 'r') as _:
        for line in _:
            n += 1
            data.add(line.strip())
    data_list = [[i, j] for i, j in enumerate(data)]
    return data_list, n


def post(data) -> list:
    # url = 'http://vegbiendev.nceas.ucsb.edu:8975/tnrs_api.php'
    url = 'https://tnrsapi.xyz/tnrs_api.php'
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'charset': 'UTF-8'}
    proxy = {'127.0.0.1': 1080}
    r = requests.post(url, data=data, headers=headers, proxies=proxy)
    print(r.headers)
    if r.status_code == 200:
        return r.json()
    else:
        print('Query failed.')
        return []


def main():
    raw = Path(argv[1])
    out = raw.with_suffix('.json')
    output = raw.with_suffix('.result.csv')
    method = 'POST'
    data, n_raw = read_csv(raw)
    print(f'{n_raw} raw records, {n_raw-len(data)} duplicated')
    opts = {'sources': 'tropicos,tpl,usda', 'matches': 'best'}
    opts_json = json.dumps(opts)
    # data json
    # [[2, "A b"],[3,[Poaceae"]]
    n_limit = 5000
    out_handle = open(out, 'a')
    for i in range(0, len(data), n_limit):
        print(i, 'to', i+n_limit,)
        batch =data[i:i+n_limit]
        data_json = json.dumps(batch)
        json_s = '{"opts":' + opts_json + ',"data":' + data_json +'}'
        result = post(json_s)
        json.dump(result, out_handle)
        out_handle.write('\n')
    with open(out, 'w', encoding='utf-8') as _:
        all_result = [json.loads(line) for line in _]
    with open(output, 'w', encoding='utf-8', newline='') as out_csv:
        fields = list(result[0].keys())
        writer = csv.DictWriter(out_csv, fieldnames=fields)
        writer.writeheader()
        for i in all_result:
            for j in i:
                writer.writerow(j)
    print('Done.')






main()