from datetime import datetime
from http import HTTPStatus

import logging as log

from api.base_api import BaseApi
from modules.constants import Data


def test_add_comment_success(tc_logger,
                             get_aut_token,
                             setup_and_teardown_news,
                             teardown_comment):
    tc_logger.log_test_name(
        "Verify successful addition of a comment to news."
    )
    comment_text = (
        f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    )
    news_id = setup_and_teardown_news

    log.info(f"Starting test {test_add_comment_success.__name__}")
    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
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

    teardown_comment(get_aut_token, response_data['id'])
    log.info(f"Test {test_add_comment_success.__name__} completed.")


def test_delete_comment_success(tc_logger,
                                get_aut_token,
                                setup_comment):
    tc_logger.log_test_name(
        "Verify successful deletion of a comment from news."
    )
    comment_id = setup_comment.json()['id']

    log.info(f"Starting test {test_delete_comment_success.__name__}")
    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/comments/{comment_id}')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    response = api.delete_data(headers=headers)
    log.info(f"Response status code: {response.status_code}")

    assert response.status_code == HTTPStatus.OK
    log.info(f"Comment with ID: {comment_id} deleted")
    log.info(f"Test {test_delete_comment_success.__name__} completed.")


def test_count_comments_success(tc_logger,
                                get_aut_token,
                                setup_and_teardown_news,
                                setup_comment,
                                teardown_comment):
    tc_logger.log_test_name(
        "Verify successful retrieval of the comment count for the news post."
    )
    news_id = setup_and_teardown_news
    comment_id = setup_comment.json()['id']

    log.info(f"Starting test {test_count_comments_success.__name__}")
    api = BaseApi(
        f'{Data.APPLICATION_API_URL}/eco-news/{news_id}/comments/count'
    )
    headers = {
        'accept': '*/*'
    }
    response = api.get_data(headers=headers)
    log.info(f"Response status code: {response.status_code}")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    log.info(f"Retrieved comment count: {response_data}")

    assert response_data == 1
    log.info("Comment count verification successful.")

    teardown_comment(get_aut_token, comment_id)
    log.info(f"Test {test_count_comments_success.__name__} completed.")


def test_update_comment_success(tc_logger,
                                get_aut_token,
                                setup_and_teardown_news,
                                setup_comment,
                                teardown_comment):
    tc_logger.log_test_name(
        "Verify successful updating of an existing comment on news."
    )
    comment_id = setup_comment.json()['id']
    modified_comment_text = (
        f'Test comment modified at '
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    )

    log.info(f"Starting test {test_update_comment_success.__name__}")
    api = BaseApi(
        f'{Data.APPLICATION_API_URL}/eco-news/comments?commentId={comment_id}'
    )
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    data = modified_comment_text
    response = api.patch_data(headers=headers, payload=data)
    log.info(f"Response status code: {response.status_code}")

    assert response.status_code == HTTPStatus.OK
    log.info(f"Comment with ID {comment_id} updated successfully.")

    teardown_comment(get_aut_token, comment_id)
    log.info(f"Test {test_update_comment_success.__name__} completed.")
