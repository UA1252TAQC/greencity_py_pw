"""
Module for holding fixtures
"""
import logging as log

import allure
import pytest

from api.base_api import BaseApi
from datetime import datetime
from modules.logger import TcLogger
from modules.constants import Data


@pytest.fixture()
def tc_logger():
    """
    A fixture that provides access to the logger object

    :return: <class 'CustomLogger'>

    Example:

    The following example will show how to use fixture in tests

    .. code-block:: python

            def test_one(tc_logger):
                tc_logger.log_test_name("test title")
    """
    return TcLogger.get_log()


@pytest.fixture(autouse=True, scope='session')
def generate_logs():
    """
    Fixture to generate log file after test run.

    The following example will show how to use fixture in tests

    .. code-block:: python

        def test_one(custom_logger):

            custom_logger.generate_logs()

            assert True
    """

    TcLogger.generate_logs()


@allure.step("Get Authorisation Token")
@pytest.fixture(scope="module")
def get_auth_token():
    """
    Fixture to get an authentication token.
    :return: Authentication token.
    """
    api = BaseApi('https://greencity-user.greencity.cx.ua/ownSecurity/signIn')
    data = {
        "email": Data.USER_EMAIL,
        "password": Data.USER_PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    log.info("CONFTEST: Requesting authentication token for user.")
    response = api.post_data(payload=data, headers=headers)
    token = response.json().get('accessToken')
    log.info("CONFTEST: Authentication token received.")

    return token


@allure.step("Setup and Teardown News")
@pytest.fixture(scope="module")
def setup_and_teardown_news(get_auth_token):
    """
    Fixture to set up and tear down a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :return: ID of the created news article.
    """
    api = BaseApi(f'{Data.BASE_URL}/eco-news')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'addEcoNewsDtoRequest': (
            '',
            '{"tags":["News"],"title":"Title Test News",'
            '"text":"Text Test News DELETE Long"}'
        )
    }
    log.info("CONFTEST: Creating a news article.")
    response = api.post_data(files=files, headers=headers)
    response_data = response.json()
    news_id = response_data['id']
    log.info(f"CONFTEST: News article created with ID: {news_id}")

    yield news_id

    log.info(f"CONFTEST: Deleting news article with ID: {news_id}")
    delete_api = BaseApi(f'{Data.BASE_URL}/eco-news/{news_id}')
    delete_api.delete_data(headers=headers)
    log.info(
        f"CONFTEST: News article with ID: {news_id} deleted successfully."
    )


@allure.step("Setup Comment")
@pytest.fixture(scope="function")
def setup_comment(get_auth_token, setup_and_teardown_news):
    """
    Fixture to create a comment for a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :param setup_and_teardown_news: Fixture that provides the news article ID.
    :return: Response of the comment creation.
    """
    news_id = setup_and_teardown_news
    comment_text = (
        f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    )

    api = BaseApi(f'{Data.BASE_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'request': ('', f'{{"parentCommentId": 0, "text": "{comment_text}"}}')
    }
    log.info(f"CONFTEST: Creating comment for news ID: {news_id}")
    response = api.post_data(files=files, headers=headers)
    log.info(f"CONFTEST: Comment created with ID: {response.json()['id']}")

    return response


@allure.step("Teardown Comment")
@pytest.fixture(scope="function")
def teardown_comment():
    """
    Fixture to delete a comment after a test.
    :return: Function to delete a comment by its ID.
    """
    def _delete_comment(get_auth_token, comment_id):
        api = BaseApi(
            f'{Data.BASE_URL}/eco-news/comments/{comment_id}'
        )
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {get_auth_token}'
        }
        log.info(f"CONFTEST: Deleting comment with ID: {comment_id}")
        api.delete_data(headers=headers)
        log.info(
            f"CONFTEST: Comment with ID: {comment_id} deleted successfully."
        )

    return _delete_comment
