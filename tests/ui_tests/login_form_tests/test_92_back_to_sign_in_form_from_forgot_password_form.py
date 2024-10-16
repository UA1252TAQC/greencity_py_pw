import allure
import logging as log

import pytest


@allure.description("Verify that the User is directed back to Sign in page after clicking the 'Back to Sign in' link")
@allure.feature("Login")
@allure.feature("Forgot Password")
@allure.issue("92")
@pytest.mark.login
@pytest.mark.forgot_password
def test_back_to_sign_in_form_from_forgot_password_form(initialize_page, tc_logger):
    test_name = "Verify that the User is directed back to Sign in page after clicking the 'Back to Sign in' link"
    tc_logger.log_test_name(test_name)
    log.info(f"Test '{test_name}' started")

    try:
        forgot_password_form = (
            initialize_page
            .header_component.open_login_form()
            .click_forgot_password_link()
        )

        log.info("Checking if the Forgot Password form is displayed.")
        assert forgot_password_form.is_forgot_password_form_displayed() is True, "Forgot Password form should be displayed."
        log.info("Forgot Password form is displayed successfully.")

        login_form = forgot_password_form.click_back_to_sign_in_link()

        log.info("Checking if the Login form is displayed after returning from Forgot Password form.")
        assert login_form.is_login_form_displayed() is True, "Login form should be displayed after clicking 'Back to Sign in'."
        log.info("Login form is displayed successfully after returning from Forgot Password form.")

        log.info(f"Test '{test_name}' completed successfully.")

    except AssertionError as ae:
        log.error(f"Assertion failed in '{test_name}': {str(ae)}")
        raise

    except Exception as e:
        log.error(f"An unexpected error occurred during '{test_name}': {str(e)}")
        raise

    finally:
        log.info(f"Test '{test_name}' finished.")
