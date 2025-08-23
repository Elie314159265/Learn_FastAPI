from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = Query(default="fixedquery", max_length=50, min_length=3,pattern="^a")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
"""
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
"""
@app.get("/items/{item_id}")
async def read_items(
        item_id: int = Path(title="The ID of the item to get"),
        q: str | None = Query(default=None, alias="item-query", deprecated=True),
        size: float | None = Query(default=1.0, lt=100.0, gt=0.0),
        ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results









