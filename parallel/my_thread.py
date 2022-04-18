#!/usr/bin/python3

from threading import Thread
from multiprocessing.pool import ThreadPool
from queue import Queue
from urllib.request import urlopen
from timeit import default_timer as timer


results = Queue()
urls = ['https://www.baidu.com', 'https://www.qq.com', 'https://www.taobao.com',
        'https://www.jd.com', 'https://www.sohu.com']
urls_queue = Queue()
for i in urls:
    urls_queue.put(i)
print(urls_queue.qsize())


def get(url):
    a = urlopen(url)
    b = a.read()
    # cannot directly get return value from Thread
    results.put((url, len(b)))
    return url, len(b)


def main():
    pool = []
    start = timer()
    for _ in range(urls_queue.qsize()):
        t = Thread(target=get, args=(urls_queue.get(),))
        pool.append(t)
        t.start()
    for t in pool:
        # sum(join) = max(join)
        t.join()
    for _ in range(results.qsize()):
        print(results.get())
    end = timer()
    print('threads', end - start)

    for i in urls:
        urls_queue.put(i)
    start = timer()
    n = urls_queue.qsize()
    print(n,'size')
    with ThreadPool(n) as p:
        p.map(get, urls)
    for _ in range(results.qsize()):
        print(results.get())
    end = timer()
    print('pool', end - start)


# in Windows, ProcessExecutorPool has to call main()
if __name__ == '__main__':
    main()