from typing import Optional, Dict

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import logging

logger = logging.getLogger("marwelove")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

_USERS_DB: Dict[str, "UserDB"] = dict()


class User(BaseModel):
    username: str


class UserDB(User):
    hashed_password: str


def hash_password(password: str) -> str:
    # TODO: rewrite, bad
    return f"hashed-{password}"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # we assume token is username
    return get_user_from_db(token)


def get_user_from_db(username: str) -> Optional[UserDB]:
    return _USERS_DB.get(username, None)


def save_user(user: UserDB) -> None:
    _USERS_DB[user.username] = user
    logger.info("Saved %s to DB", user)


def register_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    user_from_db = get_user_from_db(form_data.username)
    if user_from_db:
        raise HTTPException(status_code=400, detail="User exists")
    hashed_password = hash_password(form_data.password)
    user = UserDB(username=form_data.username, hashed_password=hashed_password)
    save_user(user)


def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    user_from_db = get_user_from_db(form_data.username)
    if not user_from_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = hash_password(form_data.password)

    if hashed_password != user_from_db.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_from_db.username, "token_type": "bearer"}
