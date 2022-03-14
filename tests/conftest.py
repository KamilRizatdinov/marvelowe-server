import pytest

"""place your fixtures here"""


@pytest.fixture
def db_setup():
    """a special fixture which cleans DB. use in tests which interact with database"""
    from src.auth import _USERS_DB
    from src.bookmarks import _BOOKMARK_CHARACTER_DB

    _USERS_DB.clear()
    _BOOKMARK_CHARACTER_DB.clear()
    yield
    _USERS_DB.clear()
    _BOOKMARK_CHARACTER_DB.clear()


@pytest.fixture
def setup_marvel_api(mocker):
    """contains useful mocks"""
    mocker.patch(
        "src.api._request_marvel_api",
        return_value={"data": {"results": [{"data": "testing information", "id": 1}]}},
    )
