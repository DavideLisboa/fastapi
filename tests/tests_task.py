from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False


def test_read_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False


def test_update_task():
    response = client.put(
        "/tasks/1", json={"title": "Updated Task", "description": "Updated Description", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True


def test_partial_update_task():
    response = client.patch("/tasks/1", json={"completed": False})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 204
