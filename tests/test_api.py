import pytest

from stats.api import RequestPayload
from stats import BadRequest


class MockRequest:
    def __init__(self, the_json):
        self._the_json = the_json

    def get_json(self):
        return self._the_json


def test_user_name():
    payload = RequestPayload(MockRequest(dict(userName='spam')))
    assert payload.get_user_name() == 'spam'


def test_user_name_missing():
    payload = RequestPayload(MockRequest(dict(notUserName='spam')))
    with pytest.raises(BadRequest):
        payload.get_user_name()


def test_user_name_wrong_type():
    payload = RequestPayload(MockRequest(dict(userName=[])))
    with pytest.raises(BadRequest):
        payload.get_user_name()


def test_number_int():
    payload = RequestPayload(MockRequest(dict(number=42)))
    assert payload.get_number() == 42


def test_number_float():
    payload = RequestPayload(MockRequest(dict(number=42.0)))
    assert payload.get_number() == 42.0


def test_number_missing():
    payload = RequestPayload(MockRequest(dict(notNumber=42)))
    with pytest.raises(BadRequest):
        payload.get_number()


def test_number_wrong_type():
    payload = RequestPayload(MockRequest(dict(number=[])))
    with pytest.raises(BadRequest):
        payload.get_number()


def test_missing_payload():
    with pytest.raises(BadRequest):
        RequestPayload(MockRequest(None))


def test_payload_wrong_type():
    with pytest.raises(BadRequest):
        RequestPayload(MockRequest([]))
