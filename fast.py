from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from database import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from utils import check_api_key

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class KeyBase(BaseModel):
    key: str

@app.get("/read-data/")
async def read_data(key: KeyBase, db: db_dependency):
    if check_api_key(key.key):
        # do something
        return {"key": "right key"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden: Access denied")
