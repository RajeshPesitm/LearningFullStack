# backend/app/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr, conint

Base = declarative_base()

# Association Table for Faculty <-> Subject (many-to-many)
faculty_subject_association = Table(
    "faculty_subjects",
    Base.metadata,
    Column("faculty_code", String(4), ForeignKey("faculties.code"), primary_key=True),
    Column("subject_code", String(10), ForeignKey("subjects.subject_code"), primary_key=True),
)

class Student(Base):
    __tablename__ = "students"

    usn = Column(String(20), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)

class Subject(Base):
    __tablename__ = "subjects"

    subject_code = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)

    faculties = relationship(
        "Faculty",
        secondary=faculty_subject_association,
        back_populates="subjects"
    )

class Faculty(Base):
    __tablename__ = "faculties"

    code = Column(String(4), primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    subjects = relationship(
        "Subject",
        secondary=faculty_subject_association,
        back_populates="faculties"
    )

# Pydantic Models
class StudentInput(BaseModel):
    usn: constr(strip_whitespace=True, min_length=10, max_length=20, pattern="^[0-9A-Z]+$")
    name: constr(strip_whitespace=True, min_length=1)
    semester: conint(ge=1, le=8)

class SubjectInput(BaseModel):
    subject_code: constr(strip_whitespace=True, min_length=3, max_length=10, pattern="^[0-9A-Z]+$")
    name: constr(strip_whitespace=True, min_length=1)
    semester: conint(ge=1, le=8)

class FacultyInput(BaseModel):
    code: constr(strip_whitespace=True, min_length=4, max_length=4, pattern="^[0-9]{4}$")
    name: constr(strip_whitespace=True, min_length=1)

