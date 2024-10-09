import pytest
import logging as log
from api.base_api import BaseApi


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

    response.raise_for_status()
    shopping_list = response.json()
    delete_habit
    assert len(shopping_list) > 0, "Expected non-empty shopping list."





