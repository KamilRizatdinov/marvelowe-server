
from collections import defaultdict
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import logging

logger = logging.getLogger("marwelove")

_BOOKMARK_CHARACTER_DB: dict[str, set[int]] = defaultdict(set)


def is_bookmarked(username:str, id: int) -> bool:
    return id in _BOOKMARK_CHARACTER_DB.get(username, [])


def get_all_character_bookmarks(username: str) -> Optional[list[int]]:
    logger.debug("Fetching %s character bookmark from DB", username)
    return list(_BOOKMARK_CHARACTER_DB.get(username, []))


def add_character_bookmark(username: str, id: int) -> None:
    if id in _BOOKMARK_CHARACTER_DB[username]:
        _BOOKMARK_CHARACTER_DB[username].remove(id)
        logger.debug("%s unbookmark character with id=%d", username, id)
    else:
        _BOOKMARK_CHARACTER_DB[username].add(id)
        logger.debug("%s bookmark character with id=%d", username, id)
