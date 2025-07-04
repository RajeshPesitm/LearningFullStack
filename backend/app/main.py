# backend/app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import database
from .models import Message, MessageInput
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


@app.post("/submit-message")
def submit_message(payload: MessageInput, db: Session = Depends(get_db)):
    new_msg = Message(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return JSONResponse(
        status_code=201,
        content={"message": "Submitted successfully", "id": new_msg.id}
    )

@app.delete("/delete-message")
def delete_message_by_email(email: str, db: Session = Depends(get_db)):
    """
    Delete the first message found with the given email.
    """
    msg = db.query(Message).filter(Message.email == email).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message with this email not found")
    db.delete(msg)
    db.commit()
    return {"status": "Deleted", "email": email}
