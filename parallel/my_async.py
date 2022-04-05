#!/usr/bin/python3

import asyncio
import aiohttp
from timeit import default_timer as timer


async def fetch(session, url):
    async with session.get(url) as r:
        data = r.status
        x = await r.text()
        return url, data


async def fetchs(session, urls):
    task = []
    for i in urls:
        t = asyncio.create_task(fetch(session, i))
        task.append(t)
    r = await asyncio.gather(*task)
    return r


async def main():
    start = timer()
    urls = ['https://www.baidu.com', 'https://www.qq.com',
            'https://www.taobao.com',
            'https://www.jd.com', 'https://www.sohu.com']
    async with aiohttp.ClientSession() as session:
        results = await fetchs(session, urls)
        for i in results:
            print(i)
    end = timer()
    print(end - start)


if __name__ == '__main__':
    # warn deprecated in python37
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
# asyncio.run(main())
