"""
外部APIを10件並列リクエストする。
・同時実行数は最大3件まで(Semaphore)
・各リクエストはタイムアウト5秒
・失敗時は3回までリトライ
"""
import asyncio
import random

SEM = asyncio.Semaphore(3)
MAX_RETRY = 3

async def fake_api_call(n: int) -> str:
    """
    外部APIへのアクセスを模した関数で50%で成功。1~3秒かかる
    """
    await asyncio.sleep(random.uniform(1,3))
    if ramdom.ramdom() < 0.5:
        raise Exception(f"API error (n={n})")
    return f"result{n}"

async def fetch_with_retry(n: int) -> str:
    """
    リトライ＋タイムアウト付きでAPIを呼び出す非同期処理
    """
    for i in range(1, MAX_RETRY + 1):
        try:
            async with SEM:
                return await asyncio.wait_for(fake_api_call(n), timeout=5)
        except Exception as e:
            print(f"[{n}] attemp {i} failed: {e}")
            if i == MAX_RETRY:
                return f"[{n}] ERROR"


async def main():
    tasks = [asyncio.create_task(fetch_with_retry(i)) for i in range(10)]
    results = asyncio.gather(*tasks)
    print("results: ", results)

if __name__ == "__main__":
    asyncio.run(main())









