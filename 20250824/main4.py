from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Annotated


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

# oauth2_schemeはここではユーザネームとして扱われる。つまりただの文字列。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# 認証されたユーザを表すモデル。実際はDBから取得する情報
class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str



# 疑似的にハッシュ化する関数(fakehashedはソルトではない...)
def fake_hash_password(password: str):
    return "fakehashed" + password

# 
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        # **user_dictはdictを展開している
        return UserInDB(**user_dict)

# 疑似トークンデコード処理。本来はJWTのようなトークンをデコードし、ユーザ情報を取り出す。
def fake_decode_token(token):
    # userにはUserInDB型が入る。
    user = get_user(fake_users_db, token)
    return user

# Depends(oauth2_scheme)によりリクエストのAuthorizationヘッダーからBearer <token>を自動取得
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # UserInDB型を代入
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 返却される型としてUserモデルを指定。つまりUserInDBのhashed_passwordは返されない
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # このシステムではtokenがusernameとして扱われる
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}