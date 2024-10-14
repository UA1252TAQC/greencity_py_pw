import allure
import pytest
from faker import Faker

from modules.constants import Data

fake = Faker()

EMPTY_FIELDS_ERROR_EN = "Please fill all required fields."
EMPTY_FIELDS_ERROR_UA = "Потрібно заповнити всі обов'язкові поля."


@allure.title("Verify Error Message for empty email and/or password")
@allure.description("This test checks the validation of the login form when email and/or password fields are empty.")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Login form")
@allure.issue("131")
@pytest.mark.parametrize(
    "language, email, password, expected",
    [
        ("Ua", '', Data.USER_PASSWORD, EMPTY_FIELDS_ERROR_UA),
        ("Ua", Data.USER_EMAIL, '', EMPTY_FIELDS_ERROR_UA),
        ("Ua", '', '', EMPTY_FIELDS_ERROR_UA),
        ("En", Data.USER_EMAIL, '', EMPTY_FIELDS_ERROR_EN),
        ("En", '', Data.USER_PASSWORD, EMPTY_FIELDS_ERROR_EN),
        ("En", '', '', EMPTY_FIELDS_ERROR_EN)
    ],
    indirect=["setup_function"]
)
def test_verify_error_message_for_empty_email_and_or_password(email,
                                                              password,
                                                              expected,
                                                              setup_function):
    login_form = setup_function

    with allure.step("Enter email and password"):
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click sign-in button and get the error message"):
        actual = login_form.click_sign_in_button().get_login_error_text()

    with allure.step("Verify error message"):
        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
