import random
import string
from http import HTTPStatus

from api.base_api import BaseApi


def generate_random_name(tc_logger, prefix="test", length=10):
    tc_logger.log_test_name(
        """Generates a random name using the given prefix and specified length
        of random characters."""
    )

    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return prefix + random_string


def test_get_categories_success(tc_logger):
    tc_logger.log_test_name("""
        Verify that the categories endpoint successfully retrieves a list of
        categories, and each category item contains all required fields,
        including specific category names.
    """)

    expected_categories = [
        "Vegan products",
        "Charging station",
        "Bike parking"
    ]

    api = BaseApi('https://greencity.greencity.cx.ua/categories')
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }

    response = api.get_data(headers=headers)
    assert response.status_code == HTTPStatus.OK, "Should return 200 OK"

    categories = response.json()
    assert isinstance(categories, list), "Response should be a list"
    assert len(categories) > 0, "List should not be empty"

    category_names = [category.get('name') for category in categories
                      if 'name' in category]

    for expected_category in expected_categories:
        assert expected_category in category_names, (
            "Expected category '{0}' not found in the response"
            .format(expected_category)
        )

    tc_logger.log_test_name(
        "Test passed: GET /categories successfully retrieved list and "
        "verified required category names"
    )


def test_create_category_success(tc_logger, get_aut_token):
    tc_logger.log_test_name("""
       Verify that the API correctly saves a new category
       and returns the expected response.
       """)
    api = BaseApi('https://greencity.greencity.cx.ua/categories')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}',
        'Content-Type': 'application/json'
    }
    unique_name = generate_random_name(tc_logger, prefix="testCat_", length=8)
    data = {
        "name": unique_name,
        "nameUa": "string",
        "parentCategoryId": 0
    }

    response = api.post_data(payload=data, headers=headers)

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert response_data['name'] == data['name'], (
        "The 'name' in the response should match the 'name' sent"
    )

    tc_logger.log_test_name(
        "Test passed: Successfully created category and verified response."
    )
