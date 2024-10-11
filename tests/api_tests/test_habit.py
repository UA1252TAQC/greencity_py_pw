from http import HTTPStatus
import pytest
import allure

from api.base_api import BaseApi
from modules.constants import Data


@pytest.mark.ui
@pytest.mark.auth
@allure.epic("Habits")
def test_get_all_habits_auth(get_auth_token, tc_logger):
    tc_logger.log_test_name("""
    Verify that the getHabit endpoint works correctly
    """)

    api = BaseApi(f'{Data.API_BASE_URL}/habit')
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token,
    }
    query_params = {'page': '0', 'size': '5'}
    response = api.get_data(headers=headers, query_params=query_params)
    json_response = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'page' in json_response
    assert 'totalElements' in json_response
    assert 'currentPage' in json_response
    assert 'totalPages' in json_response


@pytest.mark.ui
@pytest.mark.not_auth
@allure.epic("Habits")
def test_get_all_habits_notAuth(tc_logger):
    tc_logger.log_test_name("""
    Verify that the getHabit endpoint return 401 status
    for not authorized users
    """)

    api = BaseApi(f'{Data.API_BASE_URL}/habit')
    query_params = {"page": "0", "size": "5"}
    response = api.get_data(query_params=query_params)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.ui
@pytest.mark.auth
@allure.epic("Habits")
def test_get_all_habit_tags(get_auth_token, tc_logger):
    tc_logger.log_test_name("""
    Verify that the getHabitTag endpoint works correctly
    """)

    api = BaseApi(f'{Data.API_BASE_URL}/habit/tags')
    query_params = {'lang': 'en'}
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token,
    }

    response = api.get_data(headers=headers, query_params=query_params)
    json_response = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(json_response) > 0


@pytest.mark.ui
@pytest.mark.auth
@allure.epic("Habits")
def test_post_custom_habit(get_auth_token, tc_logger):
    tc_logger.log_test_name("""
    Verify that the post custom habit endpoint works correctly
    """)
    json_data = '{"habitTranslations":[{"name":"new habi\
    t","description":"<p>new habit</p><p>new habit</p><p>n\
    ew habitnew habitnew habit</p>","habitItem":"","languag\
    eCode":"ua"}],"complexity":1,"defaultDuration":13,"tagIds":\
    [11],"customShoppingListItemDto":[]}'
    fields = [
         ('request', (None, json_data))
    ]

    api = BaseApi(f'{Data.API_BASE_URL}/habit/custom')
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token
    }

    response = api.post_data(headers=headers, payload=fields)
    assert response.status_code == HTTPStatus.OK
