import json

import requests
from fastapi.testclient import TestClient
import uuid
import pytest
BASE_URL = "http://localhost:8000/"


def test_base(client_app):
    print("reached")


def test_health(client_app):
    client = TestClient(client_app)
    response = client.get(f"health")
    assert response.status_code == 200
    assert json.loads(response.content) == {"success": "Server is up and running"}


# def test_create_user(client_app):
#     client = TestClient(client_app)
#     url = f"user"
#     headers = {
#         "Content-Type": "application/json",
#     }
#
#     payload = {
#         "email": f"{str(uuid.uuid4())}@test_create_user.com",
#         "first_name": "new",
#         "last_name": "user",
#         "password": "12345678",
#     }
#
#     response = client.post(url, headers=headers, json=json.dumps(payload))
#     assert response.status_code == 201

#
# def test_login(client_app):
#     client = TestClient(client_app)
#     signup_url = f"user"
#     login_url = f"{BASE_URL}token"
#     headers = {"Content-Type": "application/json"}
#
#     email = f"{str(uuid.uuid4())}@test_create_user.com"
#     payload = {
#         "email": f"{email}",
#         "first_name": "new",
#         "last_name": "user",
#         "password": "12345678",
#     }
#
#     response = requests.post(signup_url, headers=headers, data=json.dumps(payload))
#     assert response.status_code == 201
#
#     # login request:
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "email": f"{email}",
#         "password": "12345678",
#     }
#
#     response = requests.post(login_url, headers=headers, data=json.dumps(payload))
#     assert response.status_code == 200
#     assert isinstance(response.access_token, str)
#     assert response.token_type == "bearer"
#
#
# def test_candidate_create(client_app):
#     client = TestClient(client_app)
#     url = f"{BASE_URL}candidate"
#     headers = {
#         "Content-Type": "application/json",
#         # "Authorization": auth_token,
#     }
#
#     payload = {
#         "email": f"{str(uuid.uuid4())}@test.com",
#         "first_name": "web",
#         "last_name": "developer",
#         "career_level": "Intern",
#         "job_major": "job_major",
#         "years_of_experience": 1,
#         "degree_type": "High School",
#         "skills": ["coding"],
#         "nationality": "nationality",
#         "city": "city",
#         "salary": 0,
#         "gender": "Male",
#     }
#
#     response = requests.post(url, headers=headers, data=json.dumps(payload))
#     assert response.status_code == 200
