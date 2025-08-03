# test_chapter3.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json

# テスト用のメインアプリケーション
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Optional, List

# テスト用のモデル定義
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('数量は正の値である必要があります')
        return v

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    description: Optional[str] = None
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('注文には少なくとも1つの商品が必要です')
        return v

class Order(OrderCreate):
    id: int
    total_amount: float
    status: str = "pending"
    created_at: str  # テスト用にstrで簡略化
    
    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock_quantity: int = 0

# テスト用のFastAPIアプリ
app = FastAPI(title="Chapter 3 Test App")

# テスト用データベース
fake_orders_db = {}
fake_products_db = {
    1: {"id": 1, "name": "Laptop", "description": "Gaming laptop", "price": 80000, "category": "electronics", "stock_quantity": 10},
    2: {"id": 2, "name": "Mouse", "description": "Wireless mouse", "price": 3000, "category": "electronics", "stock_quantity": 50},
    3: {"id": 3, "name": "Book", "description": "Programming book", "price": 2800, "category": "books", "stock_quantity": 20}
}
fake_users_db = {
    1: {"id": 1, "name": "Test User", "email": "test@example.com"},
    2: {"id": 2, "name": "Another User", "email": "another@example.com"}
}

# エンドポイント実装
@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    # ユーザー存在チェック
    if order.user_id not in fake_users_db:
        raise HTTPException(
            status_code=400, 
            detail=f"ユーザーID {order.user_id} が存在しません"
        )
    
    # 商品存在チェック
    for item in order.items:
        if item.product_id not in fake_products_db:
            raise HTTPException(
                status_code=400,
                detail=f"商品ID {item.product_id} が存在しません"
            )
    
    order_id = len(fake_orders_db) + 1
    total_amount = sum(item.price * item.quantity for item in order.items)
    
    order_dict = order.dict()
    order_dict.update({
        "id": order_id,
        "total_amount": total_amount,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    })
    
    fake_orders_db[order_id] = order_dict
    return order_dict

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="注文が見つかりません")
    return fake_orders_db[order_id]

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    if product_id not in fake_products_db:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    existing_product = fake_products_db[product_id].copy()
    update_data = product_update.dict(exclude_unset=True)
    existing_product.update(update_data)
    
    fake_products_db[product_id] = existing_product
    return existing_product

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id not in fake_products_db:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return fake_products_db[product_id]

# テストクライアント作成
client = TestClient(app)

# ===== テストケース =====

def test_create_order_success():
    """正常な注文作成のテスト"""
    order_data = {
        "user_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2, "price": 80000},
            {"product_id": 2, "quantity": 1, "price": 3000}
        ],
        "description": "テスト注文"
    }
    
    response = client.post("/orders", json=order_data)
    print("=== 正常な注文作成テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["total_amount"] == 163000  # (80000*2) + (3000*1)
    assert data["status"] == "pending"
    assert len(data["items"]) == 2
    print("✅ テスト合格\n")

def test_create_order_invalid_user():
    """存在しないユーザーでの注文作成テスト"""
    order_data = {
        "user_id": 999,  # 存在しないユーザー
        "items": [
            {"product_id": 1, "quantity": 1, "price": 80000}
        ]
    }
    
    response = client.post("/orders", json=order_data)
    print("=== 無効ユーザー注文テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 400
    assert "ユーザーID 999 が存在しません" in response.json()["detail"]
    print("✅ テスト合格\n")

def test_create_order_invalid_product():
    """存在しない商品での注文作成テスト"""
    order_data = {
        "user_id": 1,
        "items": [
            {"product_id": 999, "quantity": 1, "price": 1000}  # 存在しない商品
        ]
    }
    
    response = client.post("/orders", json=order_data)
    print("=== 無効商品注文テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 400
    assert "商品ID 999 が存在しません" in response.json()["detail"]
    print("✅ テスト合格\n")

def test_create_order_invalid_quantity():
    """無効な数量での注文作成テスト"""
    order_data = {
        "user_id": 1,
        "items": [
            {"product_id": 1, "quantity": 0, "price": 80000}  # 無効な数量
        ]
    }
    
    response = client.post("/orders", json=order_data)
    print("=== 無効数量注文テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 422  # バリデーションエラー
    print("✅ テスト合格\n")

def test_create_order_empty_items():
    """空の商品リストでの注文作成テスト"""
    order_data = {
        "user_id": 1,
        "items": []  # 空のリスト
    }
    
    response = client.post("/orders", json=order_data)
    print("=== 空商品リスト注文テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 422  # バリデーションエラー
    print("✅ テスト合格\n")

def test_get_order_success():
    """注文取得成功テスト"""
    # まず注文を作成
    order_data = {
        "user_id": 1,
        "items": [
            {"product_id": 3, "quantity": 5, "price": 2800}
        ],
        "description": "取得テスト用注文"
    }
    create_response = client.post("/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    # 注文を取得
    response = client.get(f"/orders/{order_id}")
    print("=== 注文取得成功テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["total_amount"] == 14000  # 2800 * 5
    print("✅ テスト合格\n")

def test_get_order_not_found():
    """存在しない注文の取得テスト"""
    response = client.get("/orders/999")
    print("=== 存在しない注文取得テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 404
    assert "注文が見つかりません" in response.json()["detail"]
    print("✅ テスト合格\n")

def test_update_product_success():
    """商品更新成功テスト"""
    update_data = {
        "name": "Updated Laptop",
        "price": 85000,
        "stock_quantity": 15
    }
    
    response = client.put("/products/1", json=update_data)
    print("=== 商品更新成功テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Laptop"
    assert data["price"] == 85000
    assert data["stock_quantity"] == 15
    assert data["category"] == "electronics"  # 更新されていないフィールドは保持
    print("✅ テスト合格\n")

def test_update_product_partial():
    """商品部分更新テスト"""
    update_data = {
        "price": 75000  # 価格のみ更新
    }
    
    response = client.put("/products/2", json=update_data)
    print("=== 商品部分更新テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 75000
    assert data["name"] == "Mouse"  # 他のフィールドは変更されない
    print("✅ テスト合格\n")

def test_update_product_not_found():
    """存在しない商品の更新テスト"""
    update_data = {
        "name": "Non-existent Product"
    }
    
    response = client.put("/products/999", json=update_data)
    print("=== 存在しない商品更新テスト ===")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 404
    assert "商品が見つかりません" in response.json()["detail"]
    print("✅ テスト合格\n")

def test_complex_order_scenario():
    """複雑な注文シナリオテスト"""
    print("=== 複雑な注文シナリオテスト ===")
    
    # 1. 複数商品の注文作成
    order_data = {
        "user_id": 2,
        "items": [
            {"product_id": 1, "quantity": 1, "price": 80000},
            {"product_id": 2, "quantity": 3, "price": 3000},
            {"product_id": 3, "quantity": 2, "price": 2800}
        ],
        "description": "複雑な注文テスト"
    }
    
    response = client.post("/orders", json=order_data)
    print(f"注文作成ステータス: {response.status_code}")
    
    assert response.status_code == 200
    order = response.json()
    expected_total = (80000 * 1) + (3000 * 3) + (2800 * 2)
    assert order["total_amount"] == expected_total
    print(f"注文ID: {order['id']}, 合計金額: {order['total_amount']}")
    
    # 2. 作成した注文を取得して確認
    order_id = order["id"]
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    
    retrieved_order = get_response.json()
    assert retrieved_order["id"] == order_id
    assert len(retrieved_order["items"]) == 3
    print(f"注文取得成功: 商品数 {len(retrieved_order['items'])}")
    print("✅ 複雑シナリオテスト合格\n")

# メイン実行部分
if __name__ == "__main__":
    print("🚀 Chapter 3 完全テスト開始\n")
    print("=" * 50)
    
    # 各テストを実行
    test_create_order_success()
    test_create_order_invalid_user()
    test_create_order_invalid_product()
    test_create_order_invalid_quantity()
    test_create_order_empty_items()
    test_get_order_success()
    test_get_order_not_found()
    test_update_product_success()
    test_update_product_partial()
    test_update_product_not_found()
    test_complex_order_scenario()
    
    print("=" * 50)
    print("🎉 全テスト完了！すべてのテストが合格しました。")
    print("\n📊 テスト結果サマリー:")
    print("- 注文作成テスト: 5件")
    print("- 注文取得テスト: 2件") 
    print("- 商品更新テスト: 3件")
    print("- 複雑シナリオテスト: 1件")
    print("- 合計: 11件のテストケース")
    print("\n✅ Chapter 3 の実装は正常に動作しています！")
