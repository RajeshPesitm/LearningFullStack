# backend/app/main.py

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.database import get_db, init_db
from app.models import Student, StudentInput, Subject, SubjectInput, Faculty, FacultyInput


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


@app.post("/student")
def add_student(student: StudentInput, db: Session = Depends(get_db)):
    s = Student(**student.model_dump())
    db.add(s)
    db.commit()
    return {"status": "Student added"}

@app.delete("/student/{usn}")
def delete_student(usn: str, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.usn == usn).first()
    if not s:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(s)
    db.commit()
    return {"status": "Student deleted"}

@app.get("/students/semester/{semester}")
def list_students(semester: int, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.semester == semester).all()

@app.post("/subject")
def add_subject(subject: SubjectInput, db: Session = Depends(get_db)):
    s = Subject(**subject.model_dump())
    db.add(s)
    db.commit()
    return {"status": "Subject added"}

@app.delete("/subject/{subject_code}")
def delete_subject(subject_code: str, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.subject_code == subject_code).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(s)
    db.commit()
    return {"status": "Subject deleted"}

@app.post("/faculty")
def add_faculty(faculty: FacultyInput, db: Session = Depends(get_db)):
    f = Faculty(**faculty.model_dump())
    db.add(f)
    db.commit()
    return {"status": "Faculty added"}

@app.delete("/faculty/{code}")
def delete_faculty(code: str, db: Session = Depends(get_db)):
    f = db.query(Faculty).filter(Faculty.code == code).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db.delete(f)
    db.commit()
    return {"status": "Faculty deleted"}

@app.get("/faculty/by-subject/{subject_code}")
def get_faculties_by_subject(subject_code: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_code == subject_code).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject.faculties

@app.get("/subject/by-faculty/{faculty_code}")
def get_subjects_by_faculty(faculty_code: str, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.code == faculty_code).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty.subjects