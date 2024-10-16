import allure
import pytest
from modules.logger import TcLogger
from tests.ui_tests.test_utils.test_data_loader_csv import get_test_data_by_test_name

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify that the ‘Sign in’ button is remained inactive after entering a invalid email and password")
@allure.description("This test checks if the 'Sign in' button is inactive when password field and email field with invalid data")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Invalid Password, Invalid Email")
@allure.issue("65")
@pytest.mark.parametrize(
    "language, email, password, expected",
    get_test_data_by_test_name('../test_data/test_data_login.csv', 'test_verify_inactive_button_for_valid_password_invalid_email')
)
def test_verify_signin_button_inactive_with_valid_password_invalid_email(language, email, password, expected, setup_function):
    logger.log_test_name(f"INFO: Starting test with valid password and invalid email for language: {language}")

    login_form = setup_function

    with allure.step("Enter valid password and invalid email"):
        logger.log_test_name("DEBUG: Entering valid password and invalid email")
        login_form.enter_email("invalid@email.com")
        login_form.enter_password("invalidpassword")

    with allure.step("Verify 'Sign in' button is inactive"):
        assert not login_form.is_sign_in_button_active(), expected
