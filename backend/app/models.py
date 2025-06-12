# backend/app/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, constr

Base = declarative_base()

# SQLAlchemy DB model
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    message = Column(Text)

# Pydantic model for input validation
class MessageInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    message: constr(strip_whitespace=True, min_length=1)
