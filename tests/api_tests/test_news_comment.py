from datetime import datetime
from http import HTTPStatus

import pytest

from api.base_api import BaseApi
from modules.constants import Data
from tests.conftest import get_aut_token, setup_and_teardown_news, setup_comment, teardown_comment


def test_add_comment_success(get_aut_token, setup_and_teardown_news, teardown_comment):
    """
    Verify successful addition of a comment to Eco News.
    """
    comment_text = f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    news_id = setup_and_teardown_news

    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    files = {
        'request': ('', f'{{"parentCommentId": 0, "text": "{comment_text}"}}')
    }
    response = api.post_data(files=files, headers=headers)
    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()

    assert response_data['text'] == comment_text
    assert response_data['author']['id'] == Data.USER_ID
    assert response_data['author']['name'] == Data.USER_NAME

    teardown_comment(get_aut_token, response_data['id'])


def test_delete_comment_success(get_aut_token, setup_comment):
    """
    Verify successful deletion of a comment from Eco News.
    """
    comment_id = setup_comment.json()['id']

    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/comments/{comment_id}')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    response = api.delete_data(headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_count_comments_success(get_aut_token, setup_and_teardown_news, setup_comment, teardown_comment):
    """
    Verify successful retrieval of the comment count for the Eco News post.
    """
    news_id = setup_and_teardown_news
    comment_id = setup_comment.json()['id']

    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/{news_id}/comments/count')
    headers = {
        'accept': '*/*'
    }
    response = api.get_data(headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == 1

    teardown_comment(get_aut_token, comment_id)


def test_update_comment_success(get_aut_token, setup_and_teardown_news, setup_comment, teardown_comment):
    """
    Verify successful updating of an existing comment on Eco News.
    """
    comment_id = setup_comment.json()['id']
    modified_comment_text = f'Test comment modified at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'

    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/comments?commentId={comment_id}')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    data = modified_comment_text
    response = api.patch_data(headers=headers, payload=data)
    assert response.status_code == HTTPStatus.OK

    teardown_comment(get_aut_token, comment_id)
