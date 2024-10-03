from http import HTTPStatus

import pytest

from api.base_api import BaseApi


@pytest.fixture()
def setup_teardown():
    api = BaseApi('https://greencity.greencity.cx.ua/categories')
    yield api


def test_get_categories_success(setup_teardown):
    """
    Verify that the categories endpoint successfully retrieves a list of categories
    and each category item contains all required fields.
    """
    api = setup_teardown
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


def test_create_category_success(setup_teardown):
    """
    Verify that the API correctly saves a new category and returns the expected response.
    """
    api = setup_teardown
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyMjZmODg1Yy1iMzZjLTQ3YmItYTQyNy01ZjY4OGY5NzhjNWNAbWFpbHNsdXJwLm5ldCIsInJvbGUiOlsiUk9MRV9VU0VSIl0sImV4cCI6MTcyNzk4MzI1MywiaWF0IjoxNzI3OTc2MDUzfQ.brJgaXWQ03jAtD9IptmhPGYw_LuY4QDNCYHFOV7f4MU',
        'Content-Type': 'application/json'
    }
    data = {
        "name": "test112",
        "nameUa": "string",
        "parentCategoryId": 0
    }

    response = api.post_data(payload=data, headers=headers)

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert 'id' in response_data, "Response should include 'id'"
    assert 'name' in response_data, "Response should include 'name'"
    assert response_data['name'] == data['name'], "The 'name' in the response should match the 'name' sent"

    print("Test passed: Successfully created category and verified response.")