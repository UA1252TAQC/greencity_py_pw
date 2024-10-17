import logging as log

import allure

from modules.constants import Data
from modules.helpers import prepare_headers

log.basicConfig(level=log.INFO)

log.basicConfig(level=log.INFO)


@allure.title("Get all shopping lists")
@allure.description("""
    This test checks the response of the request to get all shopping lists for current habit.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Shopping list")
def test_get_shopping_list_for_habit(api_client, get_auth_token, get_first_available_habit_id, delete_habit):
    """
    Test to validate the shopping list for a specific habit.
    """

    api_url = f"{Data.API_BASE_URL}/habit/{get_first_available_habit_id}/shopping-list"
    headers = prepare_headers(get_auth_token)

    log.info(f"Fetching shopping list for habit ID {get_first_available_habit_id}.")

    response = api_client.get(api_url, headers=headers)

    log.info(f"Response received: {response.json()}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    shopping_list = response.json()
    assert len(shopping_list) > 0, "Expected non-empty shopping list."

    for item in shopping_list:
        assert 'id' in item, "Each shopping list item should have an 'id' key"
        assert 'text' in item, "Each shopping list item should have a 'text' key"
        assert 'status' in item, "Each shopping list item should have a 'status' key"
        assert item['status'] == "ACTIVE", "Expected item status to be 'ACTIVE'"

    if delete_habit:
        delete_habit()
        log.info(f"Habit with ID {get_first_available_habit_id} was deleted.")
    else:
        log.warning("delete_habit is None. Skipping habit deletion.")