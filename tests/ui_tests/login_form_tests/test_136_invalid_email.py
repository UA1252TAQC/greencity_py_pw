import allure
import pytest
from faker import Faker

from modules.logger import TcLogger
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data_by_test_name, get_test_data

logger = TcLogger.get_log()

@allure.title("Verify invalid email warning after entering not valid E-mail to the 'E-mail' field")
@allure.description("This test checks the validation of the login form when email is invalid.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Sign in")
@allure.feature("Login form")
@allure.issue("136")
@pytest.mark.login
@pytest.mark.ui
@pytest.mark.parametrize(
    "setup_function_with_language, email, password, expected",
    get_test_data('../test_data/test_data_login.csv', 'test_verify_invalid_email_warning'),
    indirect=["setup_function_with_language"]
)
def test_verify_invalid_email_warning(setup_function_with_language, email, password, expected):
    login_form = setup_function_with_language

    with allure.step("Enter email and password"):
        logger.log_test_name(f"DEBUG: Entering email: '{email}' and password: '{password}'")
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click sign-in button and get the error message"):
        logger.log_test_name("INFO: Clicking sign-in button and fetching error message")
        actual = login_form.click_sign_in_button().get_email_error_text()

    with allure.step("Verify error message"):
        if actual == expected:
            logger.log_test_name(f"INFO: Verification successful. Expected: '{expected}', Actual: '{actual}'")
        else:
            logger.log_test_name(f"ERROR: Verification failed. Expected: '{expected}', but got '{actual}'")

        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
