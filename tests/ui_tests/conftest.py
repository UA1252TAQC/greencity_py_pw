import pytest

from modules.logger import TcLogger


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
