# backend/app/models.py

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, constr

Base = declarative_base()
