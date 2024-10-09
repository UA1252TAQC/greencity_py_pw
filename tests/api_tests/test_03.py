import pytest
import logging as log
from api.base_api import BaseApi

log.basicConfig(level=log.INFO)


def test_get_shopping_list_for_habit(get_auth_token, get_first_available_habit_id, delete_habit):
    """
    Test to get the shopping list for a specific habit.
    """
    api = BaseApi(f"https://greencity.greencity.cx.ua/habit/{get_first_available_habit_id}/shopping-list")
    headers = {
        'accept': '*/*',
        'Authorization': "Bearer " + get_auth_token
    }

    log.info(f"TEST: Getting shopping list for habit ID {get_first_available_habit_id}.")

    response = api.get_data(headers=headers)

    try:
        response.raise_for_status()
    except Exception as e:
        log.error(f"Error while getting shopping list: {str(e)}")
        pytest.fail(f"Request failed: {str(e)}")

    shopping_list = response.json()
    log.info(f"Received shopping list: {shopping_list}")

    assert len(shopping_list) > 0, "Expected non-empty shopping list."

    if delete_habit is not None:
        delete_habit()
        log.info(f"Habit with ID {get_first_available_habit_id} was deleted.")
    else:
        log.warning("delete_habit is None. Skipping habit deletion.")
