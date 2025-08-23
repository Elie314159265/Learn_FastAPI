from typing import Annotated, Literal
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(title="The ID of the item to get", le=100, gt=0),
        q: str | None = None,
        item: Item | None = None,
        ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results



