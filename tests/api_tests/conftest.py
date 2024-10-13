"""
Module for holding fixtures
"""
import logging as log

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
def get_first_available_habit_id(get_auth_token):
    """
    Fixture to retrieve the first available habit that has shopping list items.

    This fixture sends a request to fetch a list of habits and looks for the first habit
    that contains associated shopping list items. If no such habit is found, it raises
    a `ValueError`. It runs once per test module due to the "module" scope.

    Args:
        get_auth_token (str): The authentication token used for making the API request.

    Returns:
        int: The ID of the first habit that has shopping list items.

    Raises:
        ValueError: If the habit list is empty or no habit with shopping list items is found.
    """
    api_url = f'{Data.API_BASE_URL}/habit?page=1&size=10'
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
    Fixture to assign a habit to the user.

    This fixture sends a POST request to assign a specific habit to the user, using the
    habit ID provided by `get_first_available_habit_id`. It runs once per test module
    due to the "module" scope. The fixture logs the process and returns the assigned habit ID.

    Args:
        get_auth_token (str): The authentication token used to authorize the API request.
        get_first_available_habit_id (int): The ID of the habit to assign.

    Returns:
        int: The ID of the assigned habit, obtained from the API response.

    Raises:
        AssertionError: If the habit assignment fails (response status code not 201),
        the `handle_api_error` function is called to handle the error.
    """
    habit_id = get_first_available_habit_id
    api_url = f'{Data.API_BASE_URL}/habit/assign/{habit_id}'
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
    Fixture to retrieve the shopping list for a specific habit.

    This fixture sends a GET request to fetch the shopping list associated with the
    habit specified by `get_first_available_habit_id`. The authentication token is
    used to authorize the request, and the API response is returned in JSON format.
    If the request fails, an error handler is invoked.

    Args:
        get_auth_token (str): The authentication token used to access the API.
        get_first_available_habit_id (int): The ID of the habit for which the shopping list is fetched.

    Returns:
        dict: The API response containing the shopping list data in JSON format.

    Raises:
        AssertionError: If the API request fails (status code not 200), an error is logged
        and handled using `handle_api_error`.
    """
    api_url = f"{Data.API_BASE_URL}/habit/{get_first_available_habit_id}/shopping-list"
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
    Fixture to delete a habit that was assigned during the test.

    This fixture sends a DELETE request to the API to remove a habit that was
    assigned earlier in the test (using the `assign_habit` fixture). It runs once
    per module due to the "module" scope. The fixture logs the process and raises
    an exception if the deletion fails.

    Args:
        get_auth_token (str): The authentication token required to make the API request.
        assign_habit (int): The ID of the habit to be deleted, provided by the `assign_habit` fixture.

    Returns:
        None

    Raises:
        HTTPError: If the DELETE request fails, the fixture raises an HTTP error.
    """
    habit_id = assign_habit
    api = BaseApi(f"{Data.API_BASE_URL}/habit/assign/delete/{habit_id}")
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
    """
      Fixture to authenticate a user and retrieve their user ID.

      This fixture sends a POST request to the sign-in API using the user's credentials
      (email and password) to authenticate and retrieve the user ID. It runs once per
      test session due to the "session" scope.

      Args:
          get_auth_token (str): The authentication token used for further API requests.

      Returns:
          int: The user ID obtained from the API response after successful authentication.

      Raises:
          AssertionError: If the authentication request fails (status code not 200),
          an API error handler is invoked.
      """
    api = BaseApi(f'{Data.API_BASE_URL}/ownSecurity/signIn')
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
    """
        Fixture to fetch all user-assigned habits.

        This fixture sends a GET request to the API to retrieve the list of habits assigned
        to the user with the specified user_id. It uses the authentication token and user ID
        to prepare headers and construct the request URL.

        Args:
            get_auth_token (str): The authentication token used to access the API.
            get_user_id (int): The ID of the user whose habits need to be fetched.

        Returns:
            dict: The API response containing the user's habit data in JSON format.

        Raises:
            AssertionError: If the response status code is not 200, an API error handler is invoked.
        """
    api_url = f"{Data.API_BASE_URL}/habit/assign/allUser/{get_user_id}"
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
    Fixture to retrieve the first habit ID from the user's habits.

    This fixture accesses the user's habits and returns the ID of the first habit
    from the list. If no habits are available, it raises a test failure.

    Args:
        get_user_habits (dict): A dictionary containing the user's habit data,
        with a key 'page' that stores a list of habits.

    Returns:
        int: The ID of the first habit from the user's habit list.

    Raises:
        pytest.fail: If no habits are available in the user's habit list.
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

     This fixture provides a function that sends a DELETE request to the API to remove
     a specific shopping list item associated with a given habit. It requires both
     the habit ID and the shopping list item ID as parameters. If the deletion is
     unsuccessful, the fixture will handle the API error.

     Args:
         get_auth_token (str): The authentication token used for making API requests.

     Returns:
         function: A function that accepts two arguments:
             - habit_id (int): The ID of the habit associated with the shopping list item.
             - shopping_list_item_id (int): The ID of the shopping list item to delete.

     Raises:
         AssertionError: If the DELETE request fails (response status code is not 200),
         an API error handler is invoked.
     """
    def _delete_item(habit_id, shopping_list_item_id):
        api_url = (f"{Data.API_BASE_URL}/user/shopping-list-items?habitId={habit_id}&shoppingListItemId="
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
    Fixture to retrieve the ID of the first available shopping list item.

    This fixture checks the provided shopping list and returns the ID of the
    first item in the list. If the shopping list is empty or not available,
    it triggers a test failure.

    Args:
        get_shopping_list (list): A list of shopping items, each represented as a dictionary.

    Returns:
        int: The ID of the first shopping list item.

    Raises:
        pytest.fail: If no items are available in the shopping list.
    """
    shopping_list = get_shopping_list
    if shopping_list and len(shopping_list) > 0:
        return shopping_list[0]['id']
    else:
        pytest.fail("No shopping list items available to retrieve ID.")
