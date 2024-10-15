import allure
import pytest

from modules.logger import TcLogger

logger = TcLogger.get_log()
TcLogger.generate_logs(level="INFO", detailed_logs=True)


@allure.title("Verify opening of 'Forgot Password' form after clicking the 'Forgot password' link")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Sign In/Forgot password")
@allure.feature("Forgot password")
@allure.issue("135")
@pytest.mark.ui
def test_verify_opening_forgot_password_form(setup_function):
    login_form = setup_function

    logger.log_test_name("INFO: Starting test - Verify opening of 'Forgot Password' form")

    with allure.step("Clicking on the 'Forgot password' link"):
        logger.log_test_name("INFO: Clicking on the 'Forgot password' link")
        forgot_password_form = login_form.click_forgot_password_link()

    with allure.step("Checking if 'Forgot Password' form is visible"):
        is_form_visible = forgot_password_form.is_forgot_password_form_displayed()
        logger.log_test_name(f"INFO: Forgot password form visibility: {is_form_visible}")

    with allure.step("Verify visibility of 'Forgot Password' form"):
        assert is_form_visible, "Forgot password form should be visible, but it is not."
        logger.log_test_name("INFO: 'Forgot Password' form is visible as expected")
