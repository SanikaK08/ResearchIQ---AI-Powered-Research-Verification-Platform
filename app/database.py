from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


url= os.getenv("DATABASE_URL")

engine= create_engine(
    url,
    echo= True
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit= False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()