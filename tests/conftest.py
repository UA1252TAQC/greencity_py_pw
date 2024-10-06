import pytest

from datetime import datetime
from modules.constants import Data
from api.base_api import BaseApi


@pytest.fixture(scope="module")
def get_aut_token():
    """
    Fixture to get an authentication token.
    :return: Authentication token.
    """
    api = BaseApi(f'{Data.USER_API_URL}/ownSecurity/signIn')
    data = {
        "email": Data.EMAIL,
        "password": Data.PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    response = api.post_data(payload=data, headers=headers)
    token = response.json().get('accessToken')
    return token


@pytest.fixture(scope="module")
def setup_and_teardown_news(get_aut_token):
    """
    Fixture to set up and tear down a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :return: ID of the created news article.
    """
    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    files = {
        'addEcoNewsDtoRequest': ('', '{"tags":["News"],"title":"Title Test News","text":"Text Test News DELETE Long"}')
    }
    response = api.post_data(files=files, headers=headers)
    response_data = response.json()
    news_id = response_data['id']

    yield news_id

    delete_api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/{news_id}')
    delete_api.delete_data(headers=headers)


@pytest.fixture(scope="function")
def setup_comment(get_aut_token, setup_and_teardown_news):
    """
    Fixture to create a comment for a news article.
    :param get_aut_token: Fixture to get the authentication token.
    :param setup_and_teardown_news: Fixture that creates and provides the news article ID.
    :return: Response of the comment creation.
    """
    news_id = setup_and_teardown_news
    comment_text = f'Test comment at {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'

    api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/{news_id}/comments')
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_aut_token}'
    }
    files = {
        'request': ('', f'{{"parentCommentId": 0, "text": "{comment_text}"}}')
    }
    response = api.post_data(files=files, headers=headers)
    return response


@pytest.fixture(scope="function")
def teardown_comment():
    """
    Fixture to delete a comment after a test.
    :return: Function to delete a comment by its ID.
    """
    def _delete_comment(get_aut_token, comment_id):
        api = BaseApi(f'{Data.APPLICATION_API_URL}/eco-news/comments/{comment_id}')
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {get_aut_token}'
        }
        api.delete_data(headers=headers)

    return _delete_comment
