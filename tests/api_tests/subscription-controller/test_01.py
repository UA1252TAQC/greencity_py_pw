import requests
from http import HTTPStatus

from modules.constants import Data

BASE_URL = 'https://greencity-user.greencity.cx.ua'


def sign_in():
    url = f'{BASE_URL}/ownSecurity/signIn'
    data = {
        "email": Data.USER_EMAIL,
        "password": Data.USER_PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    return response.json()['accessToken']


# def test_create_subscription():
#     token = sign_in()
#     url = 'https://greencity.greencity.cx.ua/subscriptions'
#     api = BaseApi(url)
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "email": Data.USER_EMAIL,
#         "subscriptionType": "ECO_NEWS"
#     }
#     response = api.post_data(headers=headers, payload=data)
#     assert response.status_code == HTTPStatus.CREATED
#     json_response = response.json()
#     assert json_response["email"] == Data.EMAIL
#     assert json_response["subscriptionType"] == "ECO_NEWS"
