import pytest
import allure
import requests
from http import HTTPStatus
from api.base_api import BaseApi
from modules.constants import Data
from modules.dataprovider import DataProvider


def sign_in():
    url = f'{Data.API_BASE_URL}/ownSecurity/signIn'
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


@allure.title("Subscribe to eco news")
@allure.description("""
    This test checks the response of the request to subscribe an email to eco news.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Subscriptions")
@allure.feature("Subscribe to eco news")
@allure.story("Subscribe to eco news")
@allure.tag("Subscriptions")
@pytest.mark.parametrize(
    "email, subscription_type",
    DataProvider.get_api_test_data("test_subscribe_to_eco_news")
)
def test_subscribe_to_eco_news(email, subscription_type):
    token = sign_in()
    api = BaseApi(f"{Data.API_BASE_URL}subscriptions")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "email": email,
        "subscriptionType": subscription_type
    }
    response = api.post_data(payload=payload, headers=headers)

    assert response.status_code == HTTPStatus.CREATED

    json_response = response.json()
    assert "unsubscribeToken" in json_response


@allure.title("Unsubscribe from eco news")
@allure.description("""
    This test checks the response of the request to unsubscribe from eco news by token.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Subscriptions")
@allure.feature("Unsubscribe from eco news")
@allure.story("Unsubscribe from eco news")
@allure.tag("Subscriptions")
@pytest.mark.parametrize(
    "unsubscribe_token",
    DataProvider.get_api_test_data("test_unsubscribe_from_eco_news")
)
def test_unsubscribe_from_eco_news(unsubscribe_token):
    token = sign_in()
    api = BaseApi(f"{Data.API_BASE_URL}subscriptions/{unsubscribe_token}")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = api.delete_data(headers=headers)

    assert response.status_code == HTTPStatus.OK
