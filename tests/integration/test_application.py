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


def test_get_zero_bookmarked_characters(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    characher_response = client.get("/characters?onlyBookmarked=true", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200
    assert characher_response.json()["data"]["results"] == []


def test_get_bookmarked_characters(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    client.post(
        "/bookmark/characters/1",
        data={"username": "birdi7", "password": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    characher_response = client.get("/characters?onlyBookmarked=true", headers={"Authorization": f"Bearer {token}"})

    assert characher_response.status_code == 200
    assert characher_response.json()["data"]["results"] == [{"data": "testing information", "id": 1, "bookmark": True}]


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


def test_get_zero_bookmarked_comics(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    comics_response = client.get("/comics?onlyBookmarked=true", headers={"Authorization": f"Bearer {token}"})

    assert comics_response.status_code == 200
    assert comics_response.json()["data"]["results"] == []


def test_get_bookmarked_comics(setup_marvel_api):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    client.post(
        "/bookmark/comics/1",
        data={"username": "birdi7", "password": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    comic_response = client.get("/comics?onlyBookmarked=true", headers={"Authorization": f"Bearer {token}"})
    assert comic_response.status_code == 200
    assert comic_response.json()["data"]["results"] == [{"data": "testing information", "id": 1, "bookmark": True}]
