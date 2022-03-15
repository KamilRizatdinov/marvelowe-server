from fastapi.testclient import TestClient

from src.application import app
from src.bookmarks import get_all_character_bookmarks, get_all_comics_bookmarks

client = TestClient(app)


def test_add_get_bookmark_chapter(setup_marvel_api, db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    response = client.post(
        "/bookmark/characters/1",
        data={"username": "birdi7", "password": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get("/bookmark/characters", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["character_bookmarks"] == get_all_character_bookmarks("birdi7")


def test_get_bookmark_chapter(setup_marvel_api, db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    response = client.get("/bookmark/characters", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["character_bookmarks"] == []


def test_add_get_bookmark_comics_chapter(setup_marvel_api, db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    response = client.post(
        "/bookmark/comics/1",
        data={"username": "birdi7", "password": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get("/bookmark/comics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["comic_bookmarks"] == get_all_comics_bookmarks("birdi7")


def test_get_bookmark_comics_chapter(setup_marvel_api, db_setup):
    client.post("/register", data={"username": "birdi7", "password": "123"})
    response = client.post("/token", data={"username": "birdi7", "password": "123"})
    token = response.json()["access_token"]

    response = client.get("/bookmark/comics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["comic_bookmarks"] == []
