import asyncio
from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/hello")
async def hello():
    await asyncio.sleep(2)
    return {"message": "Hello, FastAPI!"}

@app.get("/wait_sync/{seconds}")
def wait_sync(seconds: int):
    time.sleep(seconds)
    return {"message": "done"}

@app.get("/wait_async/{seconds}")
async def wait_async(seconds: int):
    await asyncio.sleep(seconds)
    return {"message": "done"}

    
