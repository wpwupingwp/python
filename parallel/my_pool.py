#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from urllib.request import urlopen
from timeit import default_timer as timer


urls = [
    "https://www.baidu.com",
    "https://www.qq.com",
    "https://www.taobao.com",
    "https://www.jd.com",
    "https://www.sohu.com",
]


def get(url):
    a = urlopen(url)
    b = a.read()
    return url, len(b)


def main():
    start = timer()
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(get, url) for url in urls]
        for future in as_completed(futures):
            print(future.result())
    pool.shutdown(wait=True)
    end = timer()
    print("thread pool", end - start)

    start = timer()
    pool2 = ThreadPoolExecutor(max_workers=8)
    futures = [pool2.submit(get, url) for url in urls]
    pool2.shutdown(wait=True)
    for future in futures:
        print(future.result())
    end = timer()
    print("thread pool2", end - start)

    start = timer()
    pool3 = ProcessPoolExecutor(max_workers=4)
    futures3 = [pool3.submit(get, url) for url in urls]
    for future in as_completed(futures3):
        print(future.result())
    end = timer()
    print(end - start)


# in Windows, ProcessExecutorPool has to call main()
if __name__ == "__main__":
    main()
