from http import HTTPStatus
from http.client import responses

import requests

from api.base_api import BaseApi
from modules.constants import Data

def get_token():
    api = BaseApi(Data.USER_API_URL + '/ownSecurity/signIn')
    data = {
        "email": Data.EMAIL,
        "password": Data.PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    response = api.post_data(payload=data, headers=headers)
    json_response = response.json()
    return json_response["accessToken"]

def test_get_comments_by_eco_news_id():
    api = BaseApi(Data.APP_API_URL + '/eco-news/1603/comments/active')
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer ' + get_token()
    }
    response = api.get_data(headers=headers)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()

def test_add_comment():
    api = BaseApi(Data.APP_API_URL + '/eco-news/1603/comments')
    data = {
        "request": {
            "text": "string",
            "parentCommentId": 0
        }
    }
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer ' + get_token(),
        'Content-Type': 'application/json'
    }
    response = api.post_data(payload=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED

def test_like_comment():
    api = BaseApi(Data.APP_API_URL + '/eco-news/comments/like?commentId=6610')
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer ' + get_token()
    }
    response = api.post_data(headers=headers)
    assert response.status_code == HTTPStatus.OK

def test_mark_comment_as_deleted():
    api = BaseApi(Data.APP_API_URL + '/eco-news/comments/6609')
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer ' + get_token()
    }
    response = api.delete_data(headers=headers)
    assert response.status_code == HTTPStatus.OK