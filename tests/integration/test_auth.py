from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from src.application import app
from src.auth import get_user_from_db, save_user, UserDB

client = TestClient(app)


def test_register_new_user(db_setup):
    response = client.post("/register", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 200
    assert get_user_from_db("birdi7") is not None


def test_register_existing_user(db_setup):
    save_user(UserDB(username="birdi7", hashed_password="123"))

    response = client.post("/register", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 400
