from fastapi.testclient import TestClient

from src.application import app

client = TestClient(app)


def test_get_characters_no_auth(setup_marvel_api):
    characher_response = client.get("/characters")

    assert characher_response.status_code == 400


def test_get_characters_wrong_auth(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/characters", headers={"Authorization": f"Bearer {token}124"})

    assert characher_response.status_code == 400


def test_get_characters(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/characters", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200


def test_get_character(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/characters/1", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200


def test_get_comics(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/comics", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200


def test_get_comic(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/comics/1", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200
