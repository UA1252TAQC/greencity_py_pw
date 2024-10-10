import pytest
import logging as log
from api.base_api import BaseApi

log.basicConfig(level=log.INFO)


def test_get_shopping_list_for_habit(get_shopping_list, delete_habit, get_first_available_habit_id):
    """
    Test to validate the shopping list for a specific habit.
    """
    log.info(f"Received shopping list: {get_shopping_list}")

    assert len(get_shopping_list) > 0, "Expected non-empty shopping list."

    if delete_habit:
        delete_habit()
        log.info(f"Habit with ID {get_first_available_habit_id} was deleted.")
    else:
        log.warning("delete_habit is None. Skipping habit deletion.")


def test_delete_shopping_list_item(delete_shopping_list_item, get_first_shopping_list_item_id, get_first_habit_id):
    habit_id = get_first_habit_id
    shopping_list_item_id = get_first_shopping_list_item_id

    delete_shopping_list_item(habit_id, shopping_list_item_id)

    log.info(f"Shopping list item with ID {shopping_list_item_id} for habit ID {habit_id} successfully deleted.")

