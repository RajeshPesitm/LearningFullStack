# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    if engine is not None:
        return  # already initialized

    DB_URL = "mysql+pymysql://root:root@myapp-mysql:3306/myapp_db"

    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Create the DB tables
    Base.metadata.create_all(bind=engine)
