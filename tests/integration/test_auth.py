import os

from fastapi.testclient import TestClient

from src.application import app
from src.auth import UserDB, get_user_from_db, reload, save_user

client = TestClient(app)


def test_register_new_user(db_setup):
    response = client.post("/register", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 200
    assert get_user_from_db("birdi7") is not None


def test_register_existing_user(db_setup):
    save_user(UserDB(username="birdi7", hashed_password="123"))

    response = client.post("/register", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 400


def test_token_non_existing_user(db_setup):
    response = client.post("/token", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 400
    assert get_user_from_db("birdi7") is None


def test_token_existing_user(db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})

    response = client.post("/token", data={"username": "birdi7", "password": "123"})

    assert response.status_code == 200
    assert response.json()["access_token"] == get_user_from_db("birdi7").access_token


def test_token_existing_user_wrong_password(db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})

    response = client.post("/token", data={"username": "birdi7", "password": "1253"})
    assert response.status_code == 400


def test_disable_auth_env(db_setup):
    os.environ["DISABLE_AUTH"] = "1"
    reload()
    assert get_user_from_db("admin") is not None
    del os.environ["DISABLE_AUTH"]
