import logging
import sys

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.auth import login_endpoint, register_endpoint

logger = logging.getLogger("marwelove")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)

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

app.post("/token")(login_endpoint)
app.post("/register")(register_endpoint)


@app.get("/characters")
def get_characters(
    query: Optional[str] = None,
    offset: Optional[int] = None,
):
    return api.request(
        "characters", {"nameStartsWith": query} if query else None, {"offset": offset}
    )


@app.get("/characters/{id}")
def get_character(id: int):
    character_info = api.request(f"characters/{id}")
    character_comics = api.request(f"characters/{id}/comics")

    return {
        "info": character_info["data"]["results"][0],
        "comics": character_comics["data"]["results"],
    }


@app.get("/comics")
def get_comics(query: Optional[str] = None, offset: Optional[int] = None):
    return api.request(
        "comics", {"titleStartsWith": query} if query else None, {"offset": offset}
    )


@app.get("/comics/{id}")
def get_comic(id: int):
    comic_info = api.request(f"comics/{id}")
    comic_characters = api.request(f"comics/{id}/characters")

    return {
        "info": comic_info["data"]["results"][0],
        "characters": comic_characters["data"]["results"],
    }
