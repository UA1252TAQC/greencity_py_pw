import allure
import pytest
from faker import Faker

from modules.logger import TcLogger
from tests.ui_tests.login_form_tests.test_131_132_empty_email_password import EMPTY_FIELDS_ERROR_EN
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data_by_test_name

fake = Faker()

EMPTY_PASSWORD_ERROR_UA = "Будь ласка введіть пароль."
EMPTY_PASSWORD_ERROR_EN = "Password is required."

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify Error Message for empty Password field")
@allure.description("This test checks the validation of the login form when password field is empty.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Sign in")
@allure.feature("Login form")
@allure.issue("84")
@allure.issue("85")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data_by_test_name('../test_data/test_data.csv', 'test_verify_error_message_for_empty_password')
)
def test_verify_error_message_for_empty_email(language, email, password, expected, setup_function):
    login_form = setup_function

    logger.log_test_name(f"INFO: Starting test for empty password field with language: {language}")

    with allure.step("Enter password"):
        logger.log_test_name("DEBUG: Entering empty password")
        login_form.enter_password(password)

    with allure.step("Click sign-in button and get password error message"):
        logger.log_test_name("INFO: Clicking sign-in button and fetching error message")
        actual = login_form.click_outside_form().password.get_error_message()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
