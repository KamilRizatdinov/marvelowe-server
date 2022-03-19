import logging
import sys
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.utils import get_authorization_scheme_param
from starlette.responses import Response

from src import api
from src.auth import get_current_user, login_endpoint, register_endpoint
from src.bookmarks import (
    add_character_bookmark,
    add_comics_bookmark,
    get_all_character_bookmarks,
    get_all_comics_bookmarks,
    is_bookmarked,
    is_comics_bookmarked,
)

logger = logging.getLogger("marwelove")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
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


@app.middleware("http")
async def process_auth(request, call_next):
    """check auth header"""
    logger.info("in middleware, req = %s", request.url.path)
    KNOWN_EXCEPTIONS = ["register", "token"]
    if any([v in request.url.path for v in KNOWN_EXCEPTIONS]):
        logger.info("avoiding auth")
        response = await call_next(request)
        return response

    # NOTE: very similar to fastapi.security.oauth2.OAuth2PasswordBearer.__call__
    authorization: str = request.headers.get("Authorization")
    scheme, auth_param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        logger.error(
            "Not authenticated for header %s. Scheme — %s, param -%s",
            authorization,
            scheme,
            auth_param,
        )
        return Response(status_code=400, content="Not authenticated")
    logger.info("auth_param %s", auth_param)
    user = await get_current_user(auth_param)
    if not user:
        logger.error("Given token %s, no user found", auth_param)
        return Response(status_code=400, content="Not authenticated")

    response = await call_next(request)
    return response


@app.get("/characters")
async def get_characters(
    request: Request,
    query: Optional[str] = None,
    offset: Optional[int] = None,
    onlyBookmarked: bool = False,
):

    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)

    if onlyBookmarked:
        characters = api.request("characters", {"nameStartsWith": query} if query else None, {"offset": offset})

        characters["data"]["results"] = list(
            filter(lambda x: is_bookmarked(user.username, x["id"]), list(characters["data"]["results"]))
        )

        for character in characters["data"]["results"]:
            character["bookmark"] = True
    else:
        characters = api.request("characters", {"nameStartsWith": query} if query else None, {"offset": offset})

        for character in characters["data"]["results"]:
            character["bookmark"] = is_bookmarked(user.username, character["id"])

    return characters


@app.get("/characters/{id}")
async def get_character(request: Request, id: int):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    character_info = api.request(f"characters/{id}")
    character_info["data"]["results"][0]["bookmark"] = is_bookmarked(user.username, id)
    character_comics = api.request(f"characters/{id}/comics")

    return {
        "info": character_info["data"]["results"][0],
        "comics": character_comics["data"]["results"],
    }


@app.get("/comics")
async def get_comics(
    request: Request,
    query: Optional[str] = None,
    offset: Optional[int] = None,
    onlyBookmarked: bool = False,
):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)

    if onlyBookmarked:
        comics = api.request("comics", {"StartsWith": query} if query else None, {"offset": offset})

        comics["data"]["results"] = list(
            filter(lambda x: is_comics_bookmarked(user.username, x["id"]), list(comics["data"]["results"]))
        )

        for comic in comics["data"]["results"]:
            comic["bookmark"] = True
    else:
        comics = api.request("comics", {"titleStartsWith": query} if query else None, {"offset": offset})

        for comic in comics["data"]["results"]:
            comic["bookmark"] = is_comics_bookmarked(user.username, comic["id"])

    return comics


@app.get("/comics/{id}")
async def get_comic(request: Request, id: int):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    comic_info = api.request(f"comics/{id}")
    comic_info["data"]["results"][0]["bookmark"] = is_comics_bookmarked(user.username, id)
    comic_characters = api.request(f"comics/{id}/characters")

    return {
        "info": comic_info["data"]["results"][0],
        "characters": comic_characters["data"]["results"],
    }


@app.post("/bookmark/characters/{id}")
async def bookmark_character(request: Request, id: int):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    add_character_bookmark(user.username, id)
    return {}


@app.get("/bookmark/characters")
async def get_bookmark_character(request: Request):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    bookmarks = get_all_character_bookmarks(user.username)
    return {"character_bookmarks": bookmarks}


@app.post("/bookmark/comics/{id}")
async def bookmark_comic(request: Request, id: int):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    add_comics_bookmark(user.username, id)
    return {}


@app.get("/bookmark/comics")
async def get_bookmark_comic(request: Request):
    authorization: str = request.headers.get("Authorization")
    _, auth_param = get_authorization_scheme_param(authorization)
    user = await get_current_user(auth_param)
    bookmarks = get_all_comics_bookmarks(user.username)
    return {"comic_bookmarks": bookmarks}
