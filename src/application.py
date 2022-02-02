import logging
import sys

from typing import Optional, Any
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from src import api
from src.auth import login_endpoint, register_endpoint, get_current_user, oauth2_scheme

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


@app.middleware("http")
async def process_auth(request, call_next):
    """check auth header"""
    logger.info("in middleware, req = %s", request.url.path)
    if "register" not in request.url.path and "token" not in request.url.path:
        try:
            auth_param = await oauth2_scheme.__call__(request)
            logger.info("auth_param %s", auth_param)
        except HTTPException as e:
            e: Any = e
            # return Response(status_code=400, content=e.detail)  
            pass
        # 
    else:
        logger.info("avoiding auth")
    response = await call_next(request)
    return response


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
