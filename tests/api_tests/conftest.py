"""
Module for holding fixtures
"""
import pytest

from api.base_api import BaseApi
from modules.logger import TcLogger
from modules.constants import Data


@pytest.fixture()
def tc_logger():
    """
    A fixture that provides access to the logger object

    :return: <class 'CustomLogger'>

    Example:

    The following example will show how to use fixture in tests

    .. code-block:: python

            def test_one(tc_logger):
                tc_logger.log_test_name("test title")
    """
    return TcLogger.get_log()


@pytest.fixture(autouse=True, scope='session')
def generate_logs():
    """
    Fixture to generate log file after test run.

    The following example will show how to use fixture in tests

    .. code-block:: python

        def test_one(custom_logger):

            custom_logger.generate_logs()

            assert True
    """

    TcLogger.generate_logs()

@pytest.fixture(scope="module")
def get_aut_token():
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
