from datetime import datetime
from http import HTTPStatus

import logging as log

import allure
import pytest

from api.base_api import BaseApi
from modules.constants import Data


@pytest.mark.comment
@allure.feature('Add Comment Feature')
@allure.story('Add comment in Eco News')
@allure.severity(allure.severity_level.NORMAL)
def test_add_comment_success(tc_logger,
                             get_auth_token,
                             setup_and_teardown_news):
    tc_logger.log_test_name(
        "Verify successful addition of a comment to news."
    )
    comment_text = (
        f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    )
    news_id = setup_and_teardown_news

    log.info(f"Starting test {test_add_comment_success.__name__}")
    api = BaseApi(f'{Data.BASE_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}'
    }
    files = {
        'request': ('', f'{{"parentCommentId": 0, "text": "{comment_text}"}}')
    }
    response = api.post_data(files=files, headers=headers)
    log.info(f"Response status code: {response.status_code}")

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    log.info(f"Comment created with ID: {response_data['id']}")

    assert response_data['text'] == comment_text
    log.info(f"Comment text verified: {response_data['text']}")

    assert response_data['author']['id'] == Data.USER_ID
    log.info(f"Comment author ID verified: {response_data['author']['id']}")

    assert response_data['author']['name'] == Data.USER_NAME
    log.info(
        f"Comment author name verified: {response_data['author']['name']}"
    )
