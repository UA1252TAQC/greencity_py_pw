"""
Module for holding fixtures
"""
import logging as log

import allure
import pytest

from api.base_api import BaseApi
from modules.logger import TcLogger
from modules.constants import Data


@pytest.fixture()
def tc_logger():
    """
    A fixture that provides access to the logger object

    :return: <class 'CustomLogger'>

    Example:

    The following example will show how to use fixture in tests

    .. code-block:: python

            def test_one(tc_logger):
                tc_logger.log_test_name("test title")
    """
    return TcLogger.get_log()


@pytest.fixture(autouse=True, scope='session')
def generate_logs():
    """
    Fixture to generate log file after test run.

    The following example will show how to use fixture in tests

    .. code-block:: python

        def test_one(custom_logger):

            custom_logger.generate_logs()

            assert True
    """

    TcLogger.generate_logs()


@allure.step("Get Authorization Token")
@pytest.fixture(scope="session")
def get_auth_token():
    """
    Fixture to get an authentication token.
    :return: Authentication token.
    """
    api = BaseApi(f'{Data.USER_API_BASE_URL}/ownSecurity/signIn')
    data = {
        "email": Data.USER_EMAIL,
        "password": Data.USER_PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    log.info("CONFTEST: Requesting authentication token for user.")
    response = api.post_data(payload=data, headers=headers)
    token = response.json().get('accessToken')
    log.info("CONFTEST: Authentication token received.")

    return token


@pytest.fixture(scope="module")
def get_first_available_habit_id(get_auth_token):
    """
    Fixture to get a list of habits.
    :return: list of habits.
    """
    api = BaseApi('https://greencity.greencity.cx.ua/habit?page=1&size=5')
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token
    }

    log.info("CONFTEST: Requesting habit list with authentication token for user.")

    response = api.get_data(headers=headers)

    if response.status_code == 200:
        log.info("CONFTEST: Successfully retrieved habit list.")
    else:
        log.error(f"CONFTEST: Failed to retrieve habit list. Status code: {response.status_code}")

    response.raise_for_status()
    habits_list = response.json().get('page', [])

    if len(habits_list) > 0:
        for habit in habits_list:
            if habit.get('shoppingListItems'):
                return habit.get('id')
    else:
        log.warning("CONFTEST: The habit list is empty. Consider adding a habit before proceeding.")
        raise ValueError("The habit list is empty. Unable to proceed without available habits.")


@pytest.fixture(scope="module")
def assign_habit_with_id(get_auth_token, get_first_available_habit_id):
    """
    Fixture to assign a habit.
    :return: assigned habit ID.
    """
    api = BaseApi(f'https://greencity.greencity.cx.ua/habit/assign/{get_first_available_habit_id}')
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token
    }

    log.info("CONFTEST: Assigning habit with authentication token for user.")

    response = api.post_data(headers=headers)

    if response.status_code == 201:
        log.info("CONFTEST: Successfully assigned habit.")
    else:
        log.error(f"CONFTEST: Failed to assign habit. Status code: {response.status_code}")

    response.raise_for_status()
    assigned_habit_id = response.json().get('id')

    return assigned_habit_id


@pytest.fixture(scope="module")
def delete_habit(get_auth_token, assign_habit_with_id):
    """
    Fixture to delete a habit assigned during the test.
    :return: None
    """
    habit_id = assign_habit_with_id
    api = BaseApi(f"https://greencity.greencity.cx.ua/habit/assign/delete/{habit_id}")
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token
    }

    log.info(f"CONFTEST: Deleting habit with ID {habit_id}.")

    response = api.delete_data(headers=headers)

    if response.status_code == 200:
        log.info("CONFTEST: Successfully deleted habit.")
    else:
        log.error(f"CONFTEST: Failed to delete habit. Status code: {response.status_code}")

    response.raise_for_status()
