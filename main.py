from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/characters")
def get_characters():
    return api.request("characters")


@app.get("/characters/{id}")
def get_character(id: int):
    character_info = api.request(f"characters/{id}")
    character_comics = api.request(f"characters/{id}/comics")

    return {
        "info": character_info["data"]["results"][0],
        "comics": character_comics["data"]["results"],
    }


@app.get("/comics")
def get_comics():
    return api.request("comics")


@app.get("/comics/{id}")
def get_comic(id: int):
    comic_info = api.request(f"comics/{id}")
    comic_characters = api.request(f"comics/{id}/characters")

    return {
        "info": comic_info["data"]["results"][0],
        "characters": comic_characters["data"]["results"],
    }
