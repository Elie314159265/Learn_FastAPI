import asyncio
import time

#同期処理（逐次実行）バージョン
def get_burger_sync(i: int):
    time.sleep(1)
    return f"burger{i}"

def make_sequential_burgers(n: int):
    burgers = []
    for i in range(n):
        burgers.append(get_burger_sync(i))
    return burgers

#非同期処理バージョン
async def get_burger_async(i: int):
    await asyncio.sleep(1)
    return f"burger{i}"

async def make_parallel_burgers(n: int):
    tasks = [asyncio.create_task(get_burger_async(i)) for i in range(n)]
    return await asyncio.gather(*tasks)

def run():
    print("--- 同期処理で5個作る ---")
    t0 = time.time()
    burgers_sync = make_sequential_burgers(5)
    t1 = time.time()
    print(burgers_sync, f"{t1 - t0:.2f}s")

    print("--- 非同期処理で5個作る ---")
    t0 = time.time()
    burgers_async = asyncio.run(make_parallel_burgers(5))
    t1 = time.time()
    print(burgers_async, f"{t1 - t0:.2f}s")

run()



#awaitで結果をburgersに保存する前に、get_burgers(2)の処理の完了を待つ必要があることを伝える。
#awaitが機能するためには非同期処理をサポートする関数である必要がある。async def内で宣言する。
async def get_burgers(number: int):
    #ハンバーガーを作成するために非同期処理
    return ["burger"] * number

def get_sequential_burgers(number: int):
    #ハンバーガーを作成するためにシーケンシャルな処理を実行
    return ["burger"] * number

async def main():
    burgers = await get_burgers(2)
    print(burgers)

asyncio.run(main())

