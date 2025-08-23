from datetime import datetime
from pydantic import BaseModel
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
        "id": "123",
        "signup_ts": "2017-06-01 12:22",
        "friends": [1, "123", b"2"],
        }
user = User(**external_data)
print(user)



def get_full_name(first_name: str, last_name: str):
    full_name=first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))
