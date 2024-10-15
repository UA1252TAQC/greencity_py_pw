"""
Module for holding eco-news-comment-controller fixtures
"""
import json
import logging as log

import allure
import pytest

from api.base_api import BaseApi
from datetime import datetime
from modules.constants import Data


@allure.step("Setup and Teardown News")
@pytest.fixture(scope="function")
def setup_and_teardown_news(get_auth_token):
    """
    Fixture to set up and tear down a news article.
    :param get_auth_token: Fixture to get the authentication token.
    :return: ID of the created news article.
    """
    api = BaseApi(f'{Data.API_BASE_URL}/econews')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'addEcoNewsDtoRequest': (
            '',
            json.dumps({
                "title":"News Title (created for news comment controller test)",
                "text":f"News Text (created for news comment controller test at {timestamp()})",
                "tags":["News"]
            })
        )
    }
    log.info("CONFTEST: Creating a news article.")
    response = api.post_data(files=files, headers=headers)
    response_data = response.json()
    news_id = response_data['id']
    log.info(f"CONFTEST: News article created with ID: {news_id}")

    yield news_id

    log.info(f"CONFTEST: Deleting news article with ID: {news_id}")
    delete_api = BaseApi(f'{Data.API_BASE_URL}/econews/{news_id}')
    delete_api.delete_data(headers=headers)
    log.info(
        f"CONFTEST: News article with ID: {news_id} deleted successfully."
    )


@allure.step("Setup Comment")
@pytest.fixture(scope="function")
def setup_comment(get_auth_token, setup_and_teardown_news):
    """
    Fixture to create a comment for a news article.
    :param get_auth_token: Fixture to get the authentication token.
    :param setup_and_teardown_news: Fixture that provides the news article ID.
    :return: Response of the comment creation.
    """
    news_id = setup_and_teardown_news
    comment_text = generate_comment_text_with_timestamp()

    api = BaseApi(f'{Data.API_BASE_URL}/econews/comments/{news_id}')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "parentCommentId": 0,
        "text": comment_text
    }
    response = api.post_data(payload=data, headers=headers)
    log.info(f"CONFTEST: Comment created with ID: {response.json()['id']}")

    return response

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def generate_comment_text_with_timestamp():
    return f'Test comment at {timestamp()}'


