import json
from http import HTTPStatus

import pytest

from api.base_api import BaseApi


@pytest.fixture()
def setup_teardown():
    api = BaseApi('https://greencity.greencity.cx.ua/place/statuses')
    yield api


def test_api_01(setup_teardown):
    """
    Verify that PROPOSED status is in the list of statuses
    """
    api = setup_teardown
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    assert response.text == '["PROPOSED","DECLINED","APPROVED","DELETED"]'
    json_response = json.loads(response.text)
    assert json_response[0] == "PROPOSED"


def test_api_02(setup_teardown):
    """
    Verify that DECLINED status is in the list of statuses
    """
    api = setup_teardown
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    assert response.text == '["PROPOSED","DECLINED","APPROVED","DELETED"]'
    json_response = json.loads(response.text)
    assert json_response[1] == "DECLINED"


def test_api_03(setup_teardown):
    """
    Verify that APPROVED status is in the list of statuses
    """
    api = setup_teardown
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    assert response.text == '["PROPOSED","DECLINED","APPROVED","DELETED"]'
    json_response = json.loads(response.text)
    assert json_response[2] == "APPROVED"


def test_api_04(setup_teardown):
    """
    Verify that DELETED status is in the list of statuses
    """
    api = setup_teardown
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    assert response.text == '["PROPOSED","DECLINED","APPROVED","DELETED"]'
    json_response = json.loads(response.text)
    assert json_response[3] == "DELETED"
