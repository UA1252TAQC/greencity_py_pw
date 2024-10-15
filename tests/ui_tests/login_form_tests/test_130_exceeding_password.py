import allure
import pytest
from faker import Faker

from modules.constants import Data
from modules.logger import TcLogger
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data_by_test_name

fake = Faker()

EXCEEDING_PASSWORD_ERROR_UA = "Пароль повинен містити менше 20 символів без пробілів."
EXCEEDING_PASSWORD_ERROR_EN = "Password must be less than 20 characters long without spaces."

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify Error Message for exceeding password")
@allure.description("This test checks the validation of the login form fields.")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Login form")
@allure.issue("130")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data_by_test_name('../test_data/test_data_login.csv', 'test_verify_error_message_for_exceeding_password')
)
def test_verify_error_message_for_exceeding_password(language, email, password, expected, setup_function):
    password = fake.password(length=30, special_chars=True, digits=True, upper_case=True, lower_case=True)

    logger.log_test_name(f"INFO: Starting test for exceeding password with language: {language}")

    login_form = setup_function

    with allure.step("Enter email and password"):
        logger.log_test_name(f"DEBUG: Entering email: {email} and a generated password")
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click outside the form and get error message"):
        logger.log_test_name("INFO: Clicking outside the form and fetching error message")
        actual = login_form.click_outside_form().password.get_error_message()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
