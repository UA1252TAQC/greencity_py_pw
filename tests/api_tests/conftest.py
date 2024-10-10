"""
Module for holding fixtures
"""
import logging as log
from datetime import datetime

import allure
import pytest

from api.base_api import BaseApi
from modules.logger import TcLogger
from modules.constants import Data
from modules.helpers import prepare_headers, get_habit_list, handle_api_error
from modules.api_utils import post_data


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
    api = BaseApi('https://greencity-user.greencity.cx.ua/ownSecurity/signIn')
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
def setup_and_teardown_news(get_auth_token):
    """
    Fixture to set up and tear down a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :return: ID of the created news article.
    """
    api = BaseApi(f'{Data.BASE_URL}/eco-news')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'addEcoNewsDtoRequest': (
            '',
            '{"tags":["News"],"title":"Title Test News",'
            '"text":"Text Test News DELETE Long"}'
        )
    }
    log.info("CONFTEST: Creating a news article.")
    response = api.post_data(files=files, headers=headers)
    response_data = response.json()
    news_id = response_data['id']
    log.info(f"CONFTEST: News article created with ID: {news_id}")

    yield news_id

    log.info(f"CONFTEST: Deleting news article with ID: {news_id}")
    delete_api = BaseApi(f'{Data.BASE_URL}/eco-news/{news_id}')
    delete_api.delete_data(headers=headers)
    log.info(
        f"CONFTEST: News article with ID: {news_id} deleted successfully."
    )


@pytest.fixture(scope="function")
def setup_comment(get_auth_token, setup_and_teardown_news):
    """
    Fixture to create a comment for a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :param setup_and_teardown_news: Fixture that provides the news article ID.
    :return: Response of the comment creation.
    """
    news_id = setup_and_teardown_news
    comment_text = (
        f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    )

    api = BaseApi(f'{Data.BASE_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'request': ('', f'{{"parentCommentId": 0, "text": "{comment_text}"}}')
    }
    log.info(f"CONFTEST: Creating comment for news ID: {news_id}")
    response = api.post_data(files=files, headers=headers)
    log.info(f"CONFTEST: Comment created with ID: {response.json()['id']}")

    return response


@pytest.fixture(scope="function")
def teardown_comment():
    """
    Fixture to delete a comment after a test.
    :return: Function to delete a comment by its ID.
    """
    def _delete_comment(get_auth_token, comment_id):
        api = BaseApi(
            f'{Data.BASE_URL}/eco-news/comments/{comment_id}'
        )
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {get_auth_token}'
        }
        log.info(f"CONFTEST: Deleting comment with ID: {comment_id}")
        api.delete_data(headers=headers)
        log.info(
            f"CONFTEST: Comment with ID: {comment_id} deleted successfully."
        )

    return _delete_comment


@pytest.fixture(scope="module")
def get_first_available_habit_id(get_auth_token):
    """
    Fixture to get the first available habit with shopping list items.
    :return: habit ID or raises ValueError if no habits are found.
    """
    api_url = 'https://greencity.greencity.cx.ua/habit?page=1&size=10'
    headers = prepare_headers(get_auth_token)

    log.info("CONFTEST: Requesting habit list with authentication token for user.")

    habits_list = get_habit_list(api_url, headers)

    if not habits_list:
        log.warning("CONFTEST: The habit list is empty. Consider adding a habit before proceeding.")
        raise ValueError("The habit list is empty. Unable to proceed without available habits.")

    habit = next((habit for habit in habits_list if habit.get('shoppingListItems')), None)

    if habit:
        return habit.get('id')
    else:
        raise ValueError("No habit with shopping list items found.")


@pytest.fixture(scope="module")
def assign_habit(get_auth_token, get_first_available_habit_id):
    """
    Fixture to assign a habit.
    :return: assigned habit ID.
    """
    habit_id = get_first_available_habit_id
    api_url = f'https://greencity.greencity.cx.ua/habit/assign/{habit_id}'
    headers = prepare_headers(get_auth_token)

    log.info(f"CONFTEST: Assigning habit with ID {habit_id}.")

    response = post_data(api_url, headers)

    if response.status_code == 201:
        log.info("CONFTEST: Successfully assigned habit.")
        return response.json().get('id')
    else:
        handle_api_error(response, "Failed to assign habit")


@pytest.fixture
def get_shopping_list(get_auth_token, get_first_available_habit_id):
    """
    Fixture to get the shopping list for a specific habit.
    """
    api_url = f"https://greencity.greencity.cx.ua/habit/{get_first_available_habit_id}/shopping-list"
    headers = prepare_headers(get_auth_token)

    log.info(f"Fetching shopping list for habit ID {get_first_available_habit_id}.")

    api = BaseApi(api_url)
    response = api.get_data(headers=headers)

    if response.status_code != 200:
        handle_api_error(response, f"Failed to get shopping list for habit ID {get_first_available_habit_id}")

    return response.json()


@pytest.fixture(scope="module")
def delete_habit(get_auth_token, assign_habit):
    """
    Fixture to delete a habit assigned during the test.
    :return: None
    """
    habit_id = assign_habit
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


@pytest.fixture(scope="session")
def get_user_id(get_auth_token):
    api = BaseApi('https://greencity-user.greencity.cx.ua/ownSecurity/signIn')
    data = {
        "email": Data.USER_EMAIL,
        "password": Data.USER_PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }

    response = api.post_data(payload=data, headers=headers)

    if response.status_code != 200:
        handle_api_error(response, "Failed to authenticate and retrieve user ID")

    user_id = response.json().get('userId')

    log.info(f"CONFTEST: User ID ({user_id}) received.")

    return user_id


@pytest.fixture
def get_user_habits(get_auth_token, get_user_id):
    api_url = f"https://greencity.greencity.cx.ua/habit/assign/allUser/{get_user_id}"
    headers = prepare_headers(get_auth_token)

    log.info(f"Fetching habits for user ID {get_user_id}.")

    api = BaseApi(api_url)
    response = api.get_data(headers=headers)

    if response.status_code != 200:
        handle_api_error(response, f"Failed to fetch habits for user ID {get_user_id}")

    return response.json()


@pytest.fixture
def get_first_habit_id(get_user_habits):
    """
    Fixture to get the first habit ID from the user's habits.
    """
    habits = get_user_habits.get('page', [])
    if habits and len(habits) > 0:
        first_habit_id = habits[0]['habit']['id']
        log.info(f"First habit ID: {first_habit_id}")
        return first_habit_id
    else:
        pytest.fail("No habits available to retrieve ID.")


@pytest.fixture
def delete_shopping_list_item(get_auth_token):
    """
    Fixture to delete a shopping list item by habitId and shoppingListItemId.
    """

    def _delete_item(habit_id, shopping_list_item_id):
        api_url = (f"https://greencity.greencity.cx.ua/user/shopping-list-items?habitId={habit_id}&shoppingListItemId="
                   f"{shopping_list_item_id}")
        headers = prepare_headers(get_auth_token)

        log.info(f"Attempting to delete shopping list item with ID {shopping_list_item_id} for habit ID {habit_id}.")

        api = BaseApi(api_url)
        response = api.delete_data(headers=headers)

        if response.status_code != 200:
            handle_api_error(response, f"Failed to delete shopping list item with ID {shopping_list_item_id}")

        log.info(f"Successfully deleted shopping list item with ID {shopping_list_item_id} for habit ID {habit_id}.")
        return response

    return _delete_item


@pytest.fixture
def get_first_shopping_list_item_id(get_shopping_list):
    """
    Returns the first available shopping list item ID.
    """
    shopping_list = get_shopping_list
    if shopping_list and len(shopping_list) > 0:
        return shopping_list[0]['id']
    else:
        pytest.fail("No shopping list items available to retrieve ID.")
