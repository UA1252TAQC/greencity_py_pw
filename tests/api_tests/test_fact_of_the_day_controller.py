import allure
import logging as log
import pytest
from api.base_api import BaseApi
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://greencity.greencity.cx.ua"


@allure.step("Test fetching random fact of the day")
def test_random_fact_of_the_day(tc_logger):
    tc_logger.log_test_name("Verify fetching a random fact of the day.")

    lang = "en"  # Specify the desired language code
    api = BaseApi(f"{BASE_URL}/fact-of-the-day/random")

    # Query parameters for the GET request
    query_params = {'lang': lang}
    response = api.get_data(query_params=query_params)

    log.info(f"Response status code: {response.status_code}")
    assert response.status_code == HTTPStatus.OK, f"Request failed: {response.status_code} {response.text}"

    fact_data = response.json()
    assert fact_data, "Fact data is empty."
    log.info(f"Received fact data: {fact_data}")

    fact_content = fact_data.get('content', '')
    log.info(f"Extracted fact: {fact_content}")
    assert fact_content, "Fact content is empty."

    log.info("Test for random fact of the day completed successfully.")


@allure.step("Test fetching random fact of the day by tags")
def test_random_fact_of_the_day_by_tags(tc_logger, get_auth_token):
    tc_logger.log_test_name("Verify fetching a random fact of the day by tags.")

    lang = "en"  # Specify the desired language code
    api = BaseApi(f"{BASE_URL}/fact-of-the-day/random/by-tags")

    # Query parameters for the GET request
    query_params = {'lang': lang}
    headers = {}

    if get_auth_token:  # If the auth token is available, add it to the headers
        headers['Authorization'] = f'Bearer {get_auth_token}'
        log.info(f"Using auth token: {get_auth_token}")

    response = api.get_data(headers=headers, query_params=query_params)

    log.info(f"Response status code: {response.status_code}")

    if response.status_code == HTTPStatus.OK:
        fact_data = response.json()
        assert fact_data, "Fact data is empty."
        log.info(f"Received fact data: {fact_data}")

        fact_content = fact_data.get('content', '')
        log.info(f"Extracted fact: {fact_content}")
        assert fact_content, "Fact content is empty."
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        pytest.fail("Unauthorized request: Please check your authentication token or credentials.")
    else:
        pytest.fail(f"Request failed with status code {response.status_code}: {response.text}")

    log.info("Test for random fact of the day by tags completed successfully.")
