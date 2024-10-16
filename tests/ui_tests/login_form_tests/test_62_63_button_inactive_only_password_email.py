import allure
import pytest
from modules.logger import TcLogger
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data_by_test_name

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify that the 'Sign in' button remains inactive after entering only the 'Password' field")
@allure.description("This test checks if the 'Sign in' button is inactive when only the password is filled.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Enter only Password")
@allure.issue("62")
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data_by_test_name('../test_data/test_data_login.csv', 'test_verify_inactive_button_for_only_password')
)
def test_verify_signin_button_remains_inactive_with_filled_password(language, email, password, expected, setup_function):
    logger.log_test_name(f"INFO: Starting test for empty email field with language: {language}")

    login_form = setup_function

    with allure.step("Enter password"):
        logger.log_test_name("DEBUG: Entering password")
        login_form.enter_password(password)

    with allure.step("Verify 'Sign in' button is inactive"):
        assert not login_form.is_sign_in_button_active(), \
            expected


@allure.title("Verify that the 'Sign in' button remains inactive after entering only the 'Email' field")
@allure.description("This test checks if the 'Sign in' button is inactive when only the email is filled.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Enter only Email")
@allure.issue("63")
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data_by_test_name('../test_data/test_data_login.csv', 'test_verify_inactive_button_for_only_password')
)
def test_verify_signin_button_remains_inactive_with_filled_email(language, email, password, expected, setup_function):
    logger.log_test_name(f"INFO: Starting test for empty email field with language: {language}")

    login_form = setup_function

    with allure.step("Enter email"):
        logger.log_test_name("DEBUG: Entering password")
        login_form.enter_email(email)

    with allure.step("Verify 'Sign in' button is inactive"):
        assert not login_form.is_sign_in_button_active(), \
            expected
