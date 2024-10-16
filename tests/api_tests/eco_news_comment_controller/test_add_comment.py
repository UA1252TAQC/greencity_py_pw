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
                             setup_and_teardown_news,
                             generate_comment_text_with_timestamp):
    try:
        test_name = "Verify successful addition of a comment to news"
        tc_logger.log_test_name(test_name)
        log.info(f"Test '{test_name}' started")

        comment_text = generate_comment_text_with_timestamp
        news_id = setup_and_teardown_news

        log.info(f"Starting test {test_name}")
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

    except Exception as e:
        log.error(f"An error occurred: {str(e)}")
        pytest.fail(f"Test failed due to an unexpected error: {str(e)}")
