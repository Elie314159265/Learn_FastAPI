from fastapi import FastAPI, Query, Path
import asyncio
from enum import Enum
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    description: str | None = None

class ModelName(str, Enum):
    resnet = "resnet"
    alexnet = "alexnet"
    lenet = "lenet"

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int, show_details: bool = Query(default=False)):
    results = {"user_id": user_id, "show_details": show_details}
    return results

@app.get("/ml_models/{model_name}")
async def get_model(model_name: ModelName):
    results = {"model_name": model_name.value}
    if model_name.value == "resnet":
        results.update({"message": "Have some residuals"})
    else:
        results.update({"message": "Some other model"})
    return results

@app.post("/products")
async def create_product(product: Product):
    product_dict = product.dict()
    return product_dict

@app.get("/search")
async def search_product(
        keyword: str = Query(..., min_length=3, max_length=50, pattern="^.+$"),
        category: str | None = Query(None, alias="search-category"),
        page: int = Query(1, ge=1),
        ):
    results = {"keyword": keyword, "category": category, "page": page}
    return results
    
@app.put("/items/{item_id}")
async def update_item(item_update: ItemUpdate, #デフォルト値無しは最初に指定する
                      item_id: int = Path(ge=1,le=1000),
                      notify_users: bool = Query(True),
                      ):
    await asyncio.sleep(1)
    results = {"item_id": item_id, "notify_users": notify_users, **item_update.dict()}
    return results



