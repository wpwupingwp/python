#!/usr/bin/python3

import asyncio
import aiohttp
from timeit import default_timer as timer


async def fetch(session, url):
    async with session.get(url) as r:
        data = r.status
        x = await r.text()
        return url, data


async def main():
    start = timer()
    urls = [
        "https://www.baidu.com",
        "https://www.qq.com",
        "https://www.taobao.com",
        "https://www.jd.com",
        "https://www.sohu.com",
    ]
    task = []
    async with aiohttp.ClientSession() as session:
        for i in urls:
            # like thread.start()
            t = asyncio.create_task(fetch(session, i))
            task.append(t)
        # like thread.join()
        r = await asyncio.gather(*task)
        for i in r:
            print(i)
    end = timer()
    print(end - start)


if __name__ == "__main__":
    # warn deprecated in python37
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    # error in python3.10
    # asyncio.run(main())

    # ok in python3.7 and 3.10
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
