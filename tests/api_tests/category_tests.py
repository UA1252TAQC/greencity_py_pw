import random
import string
from http import HTTPStatus
# from tests.conftest import get_aut_token

from api.base_api import BaseApi


def generate_random_name(prefix="test", length=10):
    """
    Generates a random name with the given prefix and specified
     length of random characters.
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return prefix + random_string


def test_get_categories_success():
    """
    Verify that the categories endpoint successfully retrieves a list of
    categories and each category item contains all required fields.
    """
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

    required_fields = ['name', 'nameUa', 'parentCategoryId']
    for category in categories:
        for field in required_fields:
            assert field in category, f"Each item should have a '{field}'"

    print("Test passed: GET /categories successfully retrieved list")


def test_create_category_success(get_aut_token):
    """
    Verify that the API correctly saves a new category and returns
    the expected response.
    """
    api = BaseApi('https://greencity.greencity.cx.ua/categories')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}',
        'Content-Type': 'application/json'
    }
    unique_name = generate_random_name(prefix="testCat_", length=8)
    data = {
        "name": unique_name,
        "nameUa": "string",
        "parentCategoryId": 0
    }

    response = api.post_data(payload=data, headers=headers)

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert 'id' in response_data, "Response should include 'id'"
    assert 'name' in response_data, "Response should include 'name'"
    assert response_data['name'] == data['name'], \
        "The 'name' in the response should match the 'name' sent"

    # print("Test passed: Successfully created category
    # and verified response.")
