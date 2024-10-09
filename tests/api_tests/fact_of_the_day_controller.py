import pytest
import logging
from api.base_api import BaseApi  # Import BaseApi here

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("lang, expected_status", [
    ("en", 200),  # Test for English localization
    ("invalid-lang", 400),  # Test for non-existent localization
])
def test_get_fact_of_the_day(lang, expected_status):
    """
    Test getting the fact of the day based on localization.
    :param lang: language code for retrieving the fact.
    :param expected_status: expected HTTP status code.
    """
    base_url = "https://greencity.greencity.cx.ua/fact-of-the-day/random"

    logger.info(f"Testing: Checking fact of the day for language: {lang}")

    headers = {'accept': '*/*'}
    query_params = {'lang': lang}

    logger.info(f"Making API request with parameters: {query_params} and headers: {headers}")

    # Create an instance of BaseApi using the base URL
    api = BaseApi(base_url)

    # Call get_data method from the api instance
    response = api.get_data(headers=headers, query_params=query_params)

    logger.info(f"Response status: {response.status_code}, Response text: {response.text}")

    # Check if the status code matches the expected value
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, but got {response.status_code}"
