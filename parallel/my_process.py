#!/usr/bin/python3

from multiprocessing import Pool, Process, Queue, Manager
from urllib.request import urlopen
from timeit import default_timer as timer


def get(url, results):
    a = urlopen(url)
    b = a.read()
    # cannot directly get return value from Thread
    results.put((url, len(b)))
    print('results size', results.qsize())
    return url, len(b)


def main():
    # queue between processes have to use manager
    m = Manager()
    results = m.Queue()
    urls = ['https://www.baidu.com', 'https://www.qq.com',
            'https://www.taobao.com',
            'https://www.jd.com', 'https://www.sohu.com']
    urls_queue = Queue()
    for i in urls:
        urls_queue.put(i)
    pool = []

    start = timer()
    for _ in range(urls_queue.qsize()):
        p = Process(target=get, args=(urls_queue.get(), results))
        pool.append(p)
        p.start()
    # todo
    for t in pool:
        t.join()
    for _ in range(results.qsize()):
        print(results.get())
    end = timer()
    print('threads', end - start)

    for i in urls:
        urls_queue.put(i)
    start = timer()
    n = urls_queue.qsize()
    print('n', n)
    p = Pool(n)
    results2 = [p.apply_async(get, args=(urls_queue.get(), results)) for i in range(n)]
    p.close()
    p.join()
    for _ in results2:
        # apply_async use get() to get results
        print('results2', _.get())
    # queue also works
    for _ in range(results.qsize()):
        print(results.get())
    end = timer()
    print('pool', end - start)


# in Windows, ProcessExecutorPool has to call main()
if __name__ == '__main__':
    main()