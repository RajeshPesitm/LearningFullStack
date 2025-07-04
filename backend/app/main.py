# backend/app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import database
from .database import get_db

app = FastAPI()

@app.get("/")
def root():
    return {"status": "FastAPI running. DB not connected yet."}


@app.get("/init-db")
def init_db():
    try:
        database.init_db()
        return {"status": "Database initialized successfully"}
    except Exception as e:
        return {"error": str(e)}

