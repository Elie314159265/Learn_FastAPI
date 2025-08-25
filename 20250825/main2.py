from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel

# table=Trueでテーブル実体。Pydantic互換より入出力バリデーション対応
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class HeroRead(HeroBase):
    id: int 

class HeroCreate(HeroBase):
    secret_name: str

class HeroTable(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=FalseはUvicornのスレッド間アクセスを許可する。
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    # withによってスコープ終了で自動クローズ
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# スキーマ変更が増えるならAlembic。変更履歴管理可能化する。
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: SessionDep) -> HeroRead:
    db_hero = HeroTable.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[HeroRead]:
    heroes = session.exec(select(HeroTable).offset(offset).limit(limit)).all()
    return heroes

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> HeroRead:
    hero = session.get(HeroTable, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(HeroRead, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}