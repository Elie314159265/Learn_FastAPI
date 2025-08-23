from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import Body, FastAPI, Cookie, Header, status, Form
from pydantic import BaseModel, EmailStr
from typing import Annotated

app = FastAPI()

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

class FormBase(BaseModel):
    username: str

class FormData(FormBase):
    password: str
    model_config = {"extra": "forbid"}


class FormDataOut(FormBase):
    model_config = {"extra": "forbid"}
    pass

def fake_password_hasher(raw_password: str):
    return "fake_password_" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print(user_in_db)
    print("User saved!")
    return user_in_db


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.post("/login", response_model=FormDataOut)
async def login(data: Annotated[FormData, Form()]):
    return data

@app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

@app.get("/items")
async def read_items(cookies: Annotated[Cookies, Cookie()], user_agent: str | None = Header(default=None)):
    return cookies

@app.get("/items/{item_id}")
async def read_item(
        item_id: UUID,
        start_datetime: datetime = Body(),
        end_datetime: datetime = Body(),
        process_after: timedelta = Body(),
        repeat_at: time | None = Body(default=None)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
            "item_id": item_id,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "process_after": process_after,
            "repeat_at": repeat_at,
            "start_process": start_process,
            "duration": duration,
    }

