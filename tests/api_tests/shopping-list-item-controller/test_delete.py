import logging as log

log.basicConfig(level=log.INFO)


def test_delete_shopping_list_item(delete_shopping_list_item, get_first_shopping_list_item_id, get_first_habit_id):
    habit_id = get_first_habit_id
    shopping_list_item_id = get_first_shopping_list_item_id

    response = delete_shopping_list_item(habit_id, shopping_list_item_id)

    assert response.status_code == 200

    log.info(f"Shopping list item with ID {shopping_list_item_id} for habit ID {habit_id} successfully deleted.")
