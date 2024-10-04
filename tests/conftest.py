import pytest

from modules.constants import Data
from api.base_api import BaseApi

@pytest.fixture(scope="module")
def get_aut_token ():
    api = BaseApi('https://greencity-user.greencity.cx.ua/ownSecurity/signIn')
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