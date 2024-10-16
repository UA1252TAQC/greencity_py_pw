from http import HTTPStatus

import pytest

from api.base_api import BaseApi
from modules.constants import Data
import logging as log
import inspect
import allure


@allure.description("Verify successful receiving of all achievements by type \"{achievement_status}\" "
                    "and category \"{achievement_category_id}\"")
@allure.feature("Achievements")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("achievement_status, achievement_category_id", [("ACHIEVED", 1), ("UNACHIEVED", 2)])
def test_achievements_by_type_and_category(tc_logger, get_auth_token, achievement_status, achievement_category_id):
    tc_logger.log_test_name(
        "Verify achievements by type and category."
    )
    api = BaseApi(f'{Data.API_BASE_URL}/achievements')

    query_params = {"achievementStatus": achievement_status,
                    "achievementCategoryId": achievement_category_id}

    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}',
        'Content-Type': 'application/json'
    }
    response = api.get_data(headers=headers, query_params=query_params)
    log.info(f"Request URL is: {response.url}")
    log.info(f"Received status code: {response.status_code}")
    json_response = response.json()
    assert isinstance(json_response, list), (
        'response is not type list')
    achievements = dict(json_response[0])
    assert response.status_code == HTTPStatus.OK
    expected_keys = ['id', 'title', 'name', 'nameEng', 'achievementCategory', 'condition', 'progress']
    for expected_key in expected_keys:
        assert expected_key in achievements, (
            f'There is no {expected_key} in response body')
    expected_achievement_categories = ['id', 'name']
    achievement_categories = achievements.get('achievementCategory')
    for expected_achievement_category in expected_achievement_categories:
        assert expected_achievement_category in achievement_categories, (
            f'There is no {expected_achievement_category} in response body')
    log.info(f"Test is finished: {inspect.currentframe().f_code.co_name}")


@allure.description("Verify, that unauthorized error is received after request to 'achievements' with invalid token")
@allure.feature("Achievements")
@allure.severity(allure.severity_level.NORMAL)
def test_unauthorized_error_in_achievements(tc_logger):
    tc_logger.log_test_name(
        "Verify unauthorized error with invalid token in 'achievements'"
    )
    api = BaseApi(f'{Data.API_BASE_URL}/achievements')

    query_params = {"achievementStatus": "ACHIEVED",
                    "achievementCategoryId": 1}

    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer abcdefd123456"',
        'Content-Type': 'application/json'
    }
    response = api.get_data(headers=headers, query_params=query_params)
    log.info(f"Request URL is: {response.url}")
    log.info(f"Received status code: {response.status_code}")
    json_response = response.json()
    print(type(json_response))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert json_response.get("error") == "Unauthorized"
    assert len(json_response) == 4
    expected_keys = ['timestamp', 'status', 'error', 'path']
    for expected_key in expected_keys:
        assert expected_key in response.json(), f'There is no {expected_key} in response body'
    log.info(f"Test is finished: {inspect.currentframe().f_code.co_name}")
