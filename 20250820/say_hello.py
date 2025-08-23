import asyncio
import time

async def say_hello():
    for count in range(3):
        await asyncio.sleep(1)
        print (f"Hello{count}")


asyncio.run(say_hello())
