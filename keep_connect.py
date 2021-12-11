#!/usr/bin/python3

import requests
import time
import logging

log = logging.getLogger()

while True:
    a = requests.get('https://www.ibcas.ac.cn')
    log(f'{a.status_code} {a.url}')
    time.sleep(30)
    b = requests.get('https://www.baidu.com')
    log(f'{b.status_code} {b.url}')
    time.sleep(30)
