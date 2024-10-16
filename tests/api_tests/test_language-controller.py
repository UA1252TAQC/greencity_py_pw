import json
from http import HTTPStatus

import allure
import pytest

from api.base_api import BaseApi


@pytest.fixture()
def setup_teardown():
    api = BaseApi('https://greencity.greencity.cx.ua/languages/codes')
    yield api


@allure.feature('Get available languages list')
def test_get_languages_codes(tc_logger, setup_teardown):
    tc_logger.log_test_name("""
    Verify that all codes are in the list of languages codes
    """)

    api = setup_teardown
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    assert response.text == '["ua","en"]'
    json_response = json.loads(response.text)
    assert json_response[0] == "ua"
    assert json_response[1] == "en"
