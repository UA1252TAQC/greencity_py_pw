from http import HTTPStatus

from api.base_api import BaseApi
from modules.constants import Data


# @pytest.fixture()
# def setup_teardown():
#     api = BaseApi('https://greencity.greencity.cx.ua/place/statuses')
#     yield api

def test_sign_in():
    """
    Verify that the sign-in functionality works correctly
    """
    api = BaseApi(f'{Data.USER_API_BASE_URL}/ownSecurity/signIn')
    data = {
        "email": Data.USER_EMAIL,
        "password": Data.USER_PASSWORD
    }
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json'
    }
    response = api.post_data(payload=data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response["userId"] == Data.USER_ID
    assert json_response["name"] == Data.USER_NAME
    assert json_response["ownRegistrations"] is True
