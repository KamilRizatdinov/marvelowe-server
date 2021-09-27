from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api

app = FastAPI()

origins = [
    "http://localhost",
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


@app.get("/comics")
def get_comics():
    return api.request("comics")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
