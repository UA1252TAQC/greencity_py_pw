import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("lang, expected_status", [
    ("en", 200),  # Test for English localization
    ("invalid-lang", 400),  # Test for non-existent localization
])
def test_get_fact_of_the_day(fact_of_the_day_api, lang, expected_status):
    """
    Test for getting the fact of the day based on localization.
    :param fact_of_the_day_api: fixture for accessing the API.
    :param lang: language code for which to get the fact.
    :param expected_status: expected HTTP status code.
    """
    logger.info(f"Testing: Checking fact of the day for language: {lang}")
    headers = {'accept': '*/*'}
    query_params = {'lang': lang}

    logger.info(f"Making API request with parameters: {query_params} and headers: {headers}")

    response = fact_of_the_day_api.get_data(headers=headers, query_params=query_params)

    # Логируем статус ответа и текст ответа
    logger.info(f"Response status: {response.status_code}, Response text: {response.text}")

    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, but got {response.status_code}"
    if expected_status == 404:
        assert response.text == "Not Found", f"Expected 'Not Found', but got {response.text}"
