from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DRANK_URL_DATABASE = f'postgresql://{os.getenv("POSTGRES_USERNAME")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("DATABASE_NAME")}'

drank_engine = create_engine(DRANK_URL_DATABASE)

drank_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=drank_engine)

Base = declarative_base()