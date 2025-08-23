import asyncio
from fastapi import FastAPI
import aiofiles
from typing import List

app = FastAPI()

FILES = ["file1.txt","file2.txt","file3.txt"]

async def read_file(file_path: str) -> str:
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        content = await f.read()
    return content

@app.get("/read_files")
async def read_files():
    tasks: List[asyncio.Task] = [read_file(file) for file in FILES]
    results = await asyncio.gather(*tasks)
    return {file: content for file, content in zip(FILES, results)}
