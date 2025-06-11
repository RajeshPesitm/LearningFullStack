# backend/app/main.py

from fastapi import FastAPI
from . import database

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
