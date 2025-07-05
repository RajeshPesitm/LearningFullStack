# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, Depends

from app.models import Base

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    if engine is not None:
        return  # already initialized

    DB_URL = "mysql+pymysql://root:root@myapp-mysql:3306/myapp_db"

    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

# FastAPI dependency to get a DB session
def get_db():
    if SessionLocal is None:
        raise HTTPException(status_code=503, detail="Database not initialized. Call /init-db first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
