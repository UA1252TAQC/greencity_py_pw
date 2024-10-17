import allure
import pytest
import logging as log
from modules.dataprovider_utils import DataProvider


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Registration form")
@allure.story("Registration form email field validation")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, is_should_submit_form, error_message, email, username, password, repeat_password",
    DataProvider.get_ui_test_data("testEmailValidation"),
)
def test_email_validation(
        is_expected_valid,
        expected_error_message,
        is_should_submit_form,
        error_message,
        email,
        username,
        password,
        repeat_password,
        registration_form_field_setup
):
    log.info("Starting test_email_validation with email: %s", email)
    form, localization_utils = registration_form_field_setup
    form.fill_form(email, username, password, repeat_password).submit_if(is_should_submit_form)

    is_actual_valid = form.email.is_valid()
    actual_error_message = form.email.get_error_message()

    log.info("Validation result: %s, Error message: %s", is_actual_valid, actual_error_message)

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"


@allure.title("Verify registration username field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Registration form")
@allure.story("Registration form username field validation")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, username",
    DataProvider.get_ui_test_data("testUsernameValidation"),
)
def test_username_validation(
        is_expected_valid, expected_error_message, error_message, username, registration_form_field_setup
):
    log.info("Starting test_username_validation with username: %s", username)
    form, localization_utils = registration_form_field_setup
    form.enter_username(username).click_title()

    is_actual_valid = form.username.is_valid()
    actual_error_message = form.username.get_error_message()

    log.info("Validation result: %s, Error message: %s", is_actual_valid, actual_error_message)

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"


@allure.title("Verify registration password field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Registration form")
@allure.story("Registration form password field validation")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, password",
    DataProvider.get_ui_test_data("testPasswordValidation"),
)
def                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             test_password_validation(is_expected_valid, expected_error_message, error_message, password,
                             registration_form_field_setup):
    log.info("Starting test_password_validation with password: %s", password)
    form, localization_utils = registration_form_field_setup
    form.enter_password(password).click_title()

    is_actual_valid = form.password.is_valid()
    actual_error_message = form.password.get_error_message()

    log.info("Validation result: %s, Error message: %s", is_actual_valid, actual_error_message)

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"


@allure.title("Verify registration repeat password field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Registration form")
@allure.story("Registration form repeat password field validation")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, password, repeat_password",
    DataProvider.get_ui_test_data("testRepeatPasswordValidation"),
)
def test_repeat_password_validation(
        is_expected_valid,
        expected_error_message,
        error_message,
        password,
        repeat_password,
        registration_form_field_setup
):
    log.info("Starting test_repeat_password_validation with password: %s and repeat_password: %s", password, repeat_password)
    form, localization_utils = registration_form_field_setup
    form.enter_password(password)
    form.enter_repeat_password(repeat_password).click_title()

    is_actual_valid = form.repeat_password.is_valid()
    actual_error_message = form.repeat_password.get_error_message()

    log.info("Validation result: %s, Error message: %s", is_actual_valid, actual_error_message)                                                             

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"
