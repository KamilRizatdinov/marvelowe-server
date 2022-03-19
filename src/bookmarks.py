from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, Optional

logger = logging.getLogger("marwelove")

_BOOKMARK_CHARACTER_DB: Dict[str, set[int]] = defaultdict(set)
_BOOKMARK_COMICS_DB: Dict[str, set[int]] = defaultdict(set)


def is_bookmarked(username: str, id: int) -> bool:
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


def is_comics_bookmarked(username: str, id: int) -> bool:
    return id in _BOOKMARK_COMICS_DB.get(username, [])


def get_all_comics_bookmarks(username: str) -> Optional[list[int]]:
    logger.debug("Fetching %s comics bookmark from DB", username)
    return list(_BOOKMARK_COMICS_DB.get(username, []))


def add_comics_bookmark(username: str, id: int) -> None:
    if id in _BOOKMARK_COMICS_DB[username]:
        _BOOKMARK_COMICS_DB[username].remove(id)
        logger.debug("%s unbookmark comics with id=%d", username, id)
    else:
        _BOOKMARK_COMICS_DB[username].add(id)
        logger.debug("%s bookmark comics with id=%d", username, id)
