import pytest
from fastapi.testclient import TestClient
from main import api 
from pymongo import MongoClient
from bson import ObjectId

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Government Assistant API!"}

def test_add_ministry():
    ministry_data = {
        "name": "Ministry of Health",
        "description": "Responsible for healthcare policies."
    }
    response = client.post("/add-ministry", json=ministry_data)
    assert response.status_code == 200
    assert "Ministry added successfully." in response.json()["message"]

    ministry_id = response.json()["id"]
    db_client = MongoClient("mongodb://localhost:27017/")
    db = db_client["government_data"]
    ministry = db.ministries.find_one({"_id": ObjectId(ministry_id)})
    assert ministry["name"] == ministry_data["name"]

def test_add_documents():
    document_data = [
        {
            "ministry_id": "1",
            "title": "Health Policy 2024",
            "content": "This is a policy for improving healthcare."
        },
        {
            "ministry_id": "1",
            "title": "Public Health Act",
            "content": "This document outlines the public health strategy."
        }
    ]
    response = client.post("/add-documents", json=document_data)
    assert response.status_code == 200
    assert "Documents added successfully." in response.json()["message"]

def test_generate_response():
    question_data = {
        "question": "What is the healthcare policy?",
        "ministry_name": "Ministry of Health"
    }
    response = client.post("/generate-response", json=question_data)
    assert response.status_code == 200
    assert "answer" in response.json()

def test_validate_document():
    file_data = {"file": ("test_document.txt", "This is a test document for validation.", "text/plain")}
    response = client.post("/validate-document", files=file_data)
    assert response.status_code == 200
    assert "validation_result" in response.json()

def test_add_localization():
    localization_data = {
        "ministry_id": "1",
        "address": "123 Health St.",
        "city": "Health City",
        "contact": "contact@health.gov"
    }
    response = client.post("/add-localization", json=localization_data)
    assert response.status_code == 200
    assert "Localization added successfully." in response.json()["message"]

def test_add_policy():
    policy_data = {
        "ministry_id": "1",
        "title": "Public Health Policy 2024",
        "description": "This policy defines measures to improve public health."
    }
    response = client.post("/add-policy", json=policy_data)
    assert response.status_code == 200
    assert "Policy added successfully." in response.json()["message"]
