import allure
import pytest
from faker import Faker

from modules.logger import TcLogger
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data

fake = Faker()

EMPTY_FIELDS_ERROR_UA = "Потрібно заповнити всі обов'язкові поля."
EMPTY_FIELDS_ERROR_EN = "Please fill all required fields."

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify Error Message for empty email and/or password")
@allure.description("This test checks the validation of the login form when email and/or password fields are empty.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Sign in")
@allure.feature("Login form")
@allure.issue("131")
@allure.issue("132")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data('../test_data/test_data_login.csv', 'test_verify_error_message_for_empty_email_and_or_password')
)
def test_verify_error_message_for_empty_email_and_or_password(language, email, password, expected, setup_function):
    login_form = setup_function

    logger.log_test_name(f"INFO: Starting test for empty email and/or password fields with language: {language}")

    with allure.step("Enter email and password"):
        logger.log_test_name(f"DEBUG: Entering email: '{email}' and password: '{password}'")
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click sign-in button and get the error message"):
        logger.log_test_name("INFO: Clicking sign-in button and fetching error message")
        actual = login_form.click_outside_form().get_login_error_text()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
