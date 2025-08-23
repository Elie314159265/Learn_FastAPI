"""
外部APIを10件並列リクエストする。
・同時実行数は最大3件まで(Semaphore)
・各リクエストはタイムアウト5秒
・失敗時は3回までリトライ
※ CancelledError や TimeoutError を握りつぶして最後に戻す
"""

import asyncio
import random

SEM = asyncio.Semaphore(3)  # 同時に実行する数を制限
MAX_RETRY = 3               # リトライ回数

async def fake_api_call(n: int) -> str:
    """
    外部APIへのアクセスを模した関数
    ・50%の確率で失敗
    ・1〜3秒かかる
    """
    await asyncio.sleep(random.uniform(1, 3))
    if random.random() < 0.5:
        raise Exception(f"API error (n={n})")
    return f"result{n}"

async def fetch_with_retry(n: int) -> str:
    """
    リトライ＋タイムアウト付きでAPIを呼び出す非同期処理
    """
    for i in range(1, MAX_RETRY + 1):
        try:
            async with SEM:  # 同時実行上限制御
                # タイムアウト5秒
                return await asyncio.wait_for(fake_api_call(n), timeout=5)
        except asyncio.TimeoutError:
            print(f"[{n}] timeout at attempt {i}")
        except asyncio.CancelledError:
            print(f"[{n}] cancelled at attempt {i}")
        except Exception as e:
            print(f"[{n}] attempt {i} failed: {e}")
    return f"[{n}] ERROR"  # リトライ失敗時

async def main():
    # 10件同時にタスク登録
    tasks = [asyncio.create_task(fetch_with_retry(i)) for i in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    print("results:", results)

if __name__ == "__main__":
    asyncio.run(main())

