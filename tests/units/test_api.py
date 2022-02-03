import requests
from requests import Response

from src import api


def test_request_basic(setup_marvel_api):
    assert bool(api.request("hello")) is True
    assert bool(
        api.request(
            "hello", {"titleStartsWith": "123"}, id_={"id": 3}, limit={"offset": 0}
        )
    ) is True


def test_request_market_api(mocker):
    mocker.patch.object(requests, "get", return_value=Response())
    mocker.patch.object(Response, "json", return_value={})

    assert api._request_marvel_api("/", {}) == {}
