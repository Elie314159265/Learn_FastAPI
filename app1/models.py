from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"
    merchant = "merchant"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.customer

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('パスワードは8文字以上である必要があります。')
        return v

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock_quantity: int = 0

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('価格は正の値である必要があります')
        return v

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('数量は正の値である必要があります。')
        return v

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    stock_quantity: int = 0

class Order(BaseModel):
    id: int
    total_amount: float
    status: str = "pending"
    created_at: datetime

    class Config:
        orm_mode = True
    
class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItem]
    description: Optional[str] = None

    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('注文には少なくとも1つの商品が必要です。')
    
        for item in v:
            if item.product_id == 1:
                raise ValueError('No!')
        return v

class HelloWorld(BaseModel):
    hello_id: int
    hello_str: str

    @validator('hello_id')
    def hello_id_validator(cls, v):
        if v <= 0:
            raise ValueError('値は正である必要があります。')
        return v



