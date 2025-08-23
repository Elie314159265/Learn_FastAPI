from fastapi import FastAPI, Query
import asyncio
import httpx

app = FastAPI()

BASE_URL = "https://jsonplaceholder.typicode.com/todos/"

async def fetch_todo(client: httpx.AsyncClient, todo_id: int):
    response = await client.get(f"{BASE_URL}{todo_id}")
    return response.json()

@app.get("/todos")
async def get_todos(ids: str = Query(..., description="カンマ区切りのIDリスト")):
    id_list = [int(i) for i in ids.split(",")]

    async with httpx.AsyncClient() as client:
        tasks = [fetch_todo(client, i) for i in id_list]
        results = await asyncio.gather(*tasks)
    return {"todos": results}
