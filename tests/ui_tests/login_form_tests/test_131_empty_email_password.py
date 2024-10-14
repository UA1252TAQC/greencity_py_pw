import allure
import pytest
from faker import Faker

from modules.constants import Data
from modules.logger import TcLogger

fake = Faker()

EMPTY_FIELDS_ERROR_EN = "Please fill all required fields."
EMPTY_FIELDS_ERROR_UA = "Потрібно заповнити всі обов'язкові поля."

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify Error Message for empty email and/or password")
@allure.description("This test checks the validation of the login form when email and/or password fields are empty.")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Login form")
@allure.issue("131")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "language, email, password, expected",
    [
        ("Ua", '', Data.USER_PASSWORD, EMPTY_FIELDS_ERROR_UA),
        ("Ua", Data.USER_EMAIL, '', EMPTY_FIELDS_ERROR_UA),
        ("Ua", '', '', EMPTY_FIELDS_ERROR_UA),
        ("En", Data.USER_EMAIL, '', EMPTY_FIELDS_ERROR_EN),
        ("En", '', Data.USER_PASSWORD, EMPTY_FIELDS_ERROR_EN),
        ("En", '', '', EMPTY_FIELDS_ERROR_EN)
    ]
)
def test_verify_error_message_for_empty_email_and_or_password(language, email, password, expected, setup_function):
    login_form = setup_function

    logger.log_test_name(f"INFO: Starting test for empty email and/or password fields with language: {language}")

    with allure.step("Enter email and password"):
        logger.log_test_name(f"DEBUG: Entering email: '{email}' and password: '{password}'")
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click sign-in button and get the error message"):
        logger.log_test_name("INFO: Clicking sign-in button and fetching error message")
        actual = login_form.click_sign_in_button().get_login_error_text()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
