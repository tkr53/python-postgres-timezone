from fastapi import FastAPI, Depends
from sqlmodel import create_engine, SQLModel, Session
from model import Hero
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel

engine = create_engine("postgresql://user:password@db/mydatabase", connect_args={"options": "-c timezone=Asia/Tokyo"})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class HeroIn(BaseModel):
    name: str
    secret_name: str
    age: int

@app.post("/heroes")
def create_hero(hero_in: HeroIn, session: Session = Depends(get_session)):
    hero = Hero()
    hero.name = hero_in.name
    hero.secret_name = hero_in.secret_name
    hero.age = hero_in.age
    hero.updated_at = datetime.now(ZoneInfo("Asia/Tokyo"))
    print(hero.updated_at)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    print(hero.updated_at)
    return hero

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    print(hero.updated_at)
    return hero

@app.get("/heroes/{hero_id}/today")
def read_hero_today(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    return hero.updated_at.date() == datetime.now(ZoneInfo("Asia/Tokyo")).date()