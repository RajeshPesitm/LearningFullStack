# backend/app/test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app # If not running in Docker, use from .main import app
from app import database

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def init_db():
    database.init_db()

def test_add_student():
    payload = {
        "usn": "4PM22CS001",
        "name": "Alice",
        "semester": 6
    }
    r = client.post("/student", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "Student added"

def test_list_students():
    r = client.get("/students/semester/6")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(s["usn"] == "4PM22CS001" for s in data)

def test_delete_student():
    r = client.delete("/student/4PM22CS001")
    assert r.status_code == 200
    assert r.json()["status"] == "Student deleted"

def test_add_subject():
    payload = {
        "subject_code": "BCS601",
        "name": "Distributed Systems",
        "semester": 6
    }
    r = client.post("/subject", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "Subject added"

def test_add_faculty():
    payload = {
        "code": "1234",
        "name": "Prof. Smith"
    }
    r = client.post("/faculty", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "Faculty added"

def test_delete_subject():
    r = client.delete("/subject/BCS601")
    assert r.status_code == 200
    assert r.json()["status"] == "Subject deleted"

def test_delete_faculty():
    r = client.delete("/faculty/1234")
    assert r.status_code == 200
    assert r.json()["status"] == "Faculty deleted"

def test_list_students_empty():
    r = client.get("/students/semester/6")
    assert r.status_code == 200
    assert r.json() == []
