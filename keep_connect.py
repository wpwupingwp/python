#!/usr/bin/python3

import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

while True:
    c = requests.get("https://mirrors6.tuna.tsinghua.edu.cn", verify=True)
    log.info(f"{c.status_code} {c.url}")
    a = requests.get("http://www.ibcas.ac.cn")
    log.info(f"{a.status_code} {a.url}")
    time.sleep(60)
    b = requests.get("https://www.baidu.com", verify=True)
    log.info(f"{b.status_code} {b.url}")
    # a = input('pause')
    log.info(f"{b.status_code} {b.url}")
    # a = input('pause')
    time.sleep(60)
