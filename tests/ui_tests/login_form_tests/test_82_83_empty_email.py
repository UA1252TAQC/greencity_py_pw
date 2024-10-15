import allure
import pytest
from faker import Faker

from modules.logger import TcLogger
from tests.ui_tests.login_form_tests.test_131_132_empty_email_password import EMPTY_FIELDS_ERROR_EN

fake = Faker()

EMPTY_EMAIL_ERROR_UA = "Введіть пошту."
EMPTY_EMAIL_ERROR_EN = "Email is required."

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify Error Message for empty Email field")
@allure.description("This test checks the validation of the login form when email field is empty.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Sign in")
@allure.feature("Login form")
@allure.issue("82")
@allure.issue("83")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "language, email, expected",
    [
        ("Ua", '', EMPTY_EMAIL_ERROR_UA),
        ("En", '', EMPTY_FIELDS_ERROR_EN)
    ]
)
def test_verify_error_message_for_empty_email(language, email, expected, setup_function):
    login_form = setup_function

    logger.log_test_name(f"INFO: Starting test for empty email field with language: {language}")

    with allure.step("Enter email"):
        logger.log_test_name("DEBUG: Entering empty email")
        login_form.enter_email(email)

    with allure.step("Click sign-in button and get the email error message"):
        logger.log_test_name("INFO: Clicking sign-in button and fetching error message")
        actual = login_form.click_outside_form().email.get_error_message()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
