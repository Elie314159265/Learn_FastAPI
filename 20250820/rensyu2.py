import asyncio
#回答
async def fetch_data(id):
    await asyncio.sleep(1)
    return f"data{id}"

async def main():
    #asyncio.create_taskでfetch_dataを3つtasksに入れる。
    #tasks = [fetch_data]
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1,4,1)]
    #asyncio.gatherが一気に3つの非同期タスクを実行＆完了待ちにしてくれる。
    return await asyncio.gather(*tasks)

async_data = asyncio.run(main())
print(async_data)


#模範解答
async def fetch1(i: int):
    await asyncio.sleep(1)
    return f"data{i}"

async def main1():
    return await asyncio.gather(*(fetch1(i) for i in range(1,4))) #必ず霜asyncio.create_task()は必須ではない。

print(asyncio.run(main1()))

import time
def process_sync(n: int):
    time.sleep(1)
    return f"item{n}"

async def process_async(n: int):
    await asyncio.sleep(1)
    return f"item{n}"

def run_sync():
    result_list = [process_sync(i) for i in range(5)]
    return result_list

async def run_async():
    return await asyncio.gather(*(process_async(i) for i in range(5)))

t0=time.time()
print(run_sync())
t1=time.time()
print(asyncio.run(run_async()))
t2=time.time()
print (f"delta time: {t2 + t0 - 2 * t1}")






