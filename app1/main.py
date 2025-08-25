from fastapi import FastAPI, HTTPException
from typing import Optional
from enum import Enum
from datetime import datetime
from app.models import User, UserCreate, Product, ProductCreate, Order, OrderCreate

fake_users_db = {}
fake_products_db = {}
fake_orders_db = {}



app = FastAPI(
        title = "FastAPI学習",
        description="FastAPI学習のためのハンズオン学習",
        version="1.0.0"
)



@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    user_id = len(fake_users_db) + 1
    user_dict = user.dict()
    user_dict.update({
        "id": user_id,
        "created_at": datetime.now(),
        "is_active": True
        })
    del user_dict["password"]

    fake_users_db[user_id] = user_dict
    return user_dict

@app.get("/users/{user_id}",response_model=User)
def get_user(user_id: int):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="ユーザが見つかりません")
    return fake_users_db[user_id]

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    product_id = len(fake_products_db) + 1
    product_dict = product.dict()
    product_dict["id"] = product_id

    fake_products_db[product_id] = product_dict
    return product_dict

@app.get("/products/{product_id}",response_model=Product)
def get_product(product_id: int):
    if product_id not in fake_products_db:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return fake_products_db[product_id]

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    order_id = len(fake_orders_db) + 1
    total_amount=sum(item.price * item.quantity for item in order.items)

    order_dict = order.dict()
    order_dict.update({
        "id": order_id,
        "total_amount": total_amount,
        "status": "pending",
        "created_at": datetime.now()
        })


    fake_orders_db[order_id] = order_dict
    return order_dict

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="注文が見つかりません")
    return fake_orders_db[order_id]






@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

class ItemType(str, Enum):
    electronics= "electronics"
    clothing = "clothing"
    books = "books"

@app.get("/categories/{category}")
def get_category(category: ItemType):
    return {"category": category}

@app.get("/search")
def search_items(q: Optional[str] = None, limit: int = 10, offset: int = 0):
    results = {"query": q, "limit": limit, "offset": offset}
    if q:
        results["message"] = f"Searching for {q}"
    return results

@app.get("/items")
def list_items(
        skip: int=0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
        ):
    filters = {
            "skip": skip,
            "limit": limit,
            "category": category,
            "min_price": min_price,
            "max_price": max_price
            }
    return {"filters": filters, "items": ["sample_item_1", "sample_item_2"]}

#２．商品一覧
@app.get("/products")
def get_product_list():
    return {"products": list(fake_products_db.values())}




@app.get("/health")
def health_check():
    return {"status": "healthy"}


