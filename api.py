import requests
import time
import hashlib
import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://gateway.marvel.com/v1/public/characters"
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")


def request(path, starts_with=None, id=None, limit=None):
    ts = str(int(time.time()))
    m_hash = hashlib.md5()
    ts_str_byte = bytes(ts, "utf-8")
    private_key_byte = bytes(PRIVATE_KEY, "utf-8")
    public_key_byte = bytes(PUBLIC_KEY, "utf-8")
    m_hash.update(ts_str_byte + private_key_byte + public_key_byte)
    m_hash_str = str(m_hash.hexdigest())

    payload = {"ts": ts, "apikey": PUBLIC_KEY, "hash": m_hash_str}

    if starts_with:
        payload.update(starts_with)
    
    if id:
        payload.update(id)
    
    if limit: 
        payload.update(limit)

    r = requests.get(
        f"https://gateway.marvel.com/v1/public/{path}", 
        params=payload
    )

    return r.json()
