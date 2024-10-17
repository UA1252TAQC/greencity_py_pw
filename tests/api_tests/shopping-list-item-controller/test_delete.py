import logging as log

import allure

from modules.api_utils import delete_data, get_data
from modules.constants import Data
from modules.helpers import prepare_headers

log.basicConfig(level=log.INFO)

@allure.title("Delete shopping list item")
@allure.description("""
    This test checks the response of the request to delete a shopping list item for the current habit.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Shopping list")
def test_delete_shopping_list_item(get_auth_token, get_first_shopping_list_item_id, get_first_habit_id):
    habit_id = get_first_habit_id
    shopping_list_item_id = get_first_shopping_list_item_id

    api_url = (f"{Data.API_BASE_URL}/user/shopping-list-items?habitId={habit_id}&shoppingListItemId="
               f"{shopping_list_item_id}")
    headers = prepare_headers(get_auth_token)

    log.info(f"Attempting to delete shopping list item with ID {shopping_list_item_id} for habit ID {habit_id}.")

    response = delete_data(api_url, headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    log.info(f"Shopping list item with ID {shopping_list_item_id} for habit ID {habit_id} successfully deleted.")

    get_url = f"{Data.API_BASE_URL}/habits/{habit_id}/shopping-lists"
    get_response = get_data(get_url, headers)
    shopping_list = get_response.json()

    deleted_item = next((item for item in shopping_list if item['id'] == shopping_list_item_id), None)
    assert deleted_item is None, f"Item with ID {shopping_list_item_id} was not deleted."

    log.info(f"Verified that shopping list item with ID {shopping_list_item_id} no longer exists.")
