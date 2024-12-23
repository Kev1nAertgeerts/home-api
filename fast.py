from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from database import models
from datetime import date, datetime
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, Date, cast,func
from utils import check_api_key, create_nested_dict

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class MemberBase(BaseModel):
    first_name: str
    last_name: str

class DrinkBase(BaseModel):
    name: str
    price: int

class ConsumptionRequestData(BaseModel):
    first_name: str
    name: str  # Drink name

class PriceBase(BaseModel):
    price: float
    name: str

class KeyBase(BaseModel):
    key: str

class DateBase(BaseModel):
    date: date

@app.get("/read-data/")
async def read_data(key: KeyBase, db: db_dependency):
    if check_api_key(key.key):
        # do something
        return {"key": "right key"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: Access denied")

###### DRANK #######

@app.post("/add-member/")
async def add_member(member: MemberBase, db: db_dependency):
    db_member = models.Member(first_name=member.first_name, last_name=member.last_name)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

@app.post("/add-price/")
async def add_price(price: PriceBase, db: db_dependency):
    db_price = models.Price(price = price.price, name = price.name)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)

@app.post("/add-drink/")
async def add_drink(drink: DrinkBase, db: db_dependency):
    db_price = models.Drink(price = drink.price, name = drink.name)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)

@app.get("/get-members/")
async def get_members(db: db_dependency):
    s = select(models.Member)
    rp = db.execute(s)
    
    return [dict(row._mapping) for row in rp.fetchall()]

@app.get("/get-drinks/")
async def get_drinks(db: db_dependency):
    s = select(models.Drink)
    rp = db.execute(s)
    
    return [dict(row._mapping) for row in rp.fetchall()]

@app.post("/make-consumption/")
async def make_consumption(data: ConsumptionRequestData, db: db_dependency):
    s_member = select(models.Member).where(models.Member.first_name.like(data.first_name))
    rp_member = db.execute(s_member)
    f_member = [dict(row._mapping) for row in rp_member.fetchall()]
    member_id = f_member[0]["Member"].id

    s_drink = select(models.Drink).where(models.Drink.name.like(data.name))
    rp_drink = db.execute(s_drink)
    f_drink = [dict(row._mapping) for row in rp_drink.fetchall()]
    drink_id = f_drink[0]["Drink"].id

    db_consumption = models.Consumption(member = member_id, drink = drink_id)
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)

    return {"member": f_member, "drink": f_drink}


@app.get("/get-oneday/")
async def get_today(data: DateBase, db: db_dependency):
    s = select(models.Consumption).filter(cast(models.Consumption.date,Date) == data.date)
    rp = db.execute(s)
    data = [dict(row._mapping) for row in rp.fetchall()]
 
    summed_consumptions = create_nested_dict(data)
    
    s = select(models.Member)
    rp = db.execute(s)
    members = [dict(row._mapping) for row in rp.fetchall()]

    s = select(models.Drink)
    rp = db.execute(s)
    drinks = [dict(row._mapping) for row in rp.fetchall()]
    
    return {"summed_consumptions":summed_consumptions, "drinks":drinks, "members": members}
    