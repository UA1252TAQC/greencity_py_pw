import pytest
import allure

from modules.constants import Data
from faker import Faker

fake = Faker()

INVALID_PASSWORD_ERROR_UA = "Введено невірний email або пароль."
INVALID_PASSWORD_ERROR_EN = "Bad email or password."

@allure.title("Verify Error Message for invalid password")
@allure.description("This test checks the validation of the login form fields.")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Login form")
@allure.issue("128")
@pytest.mark.parametrize(
    "language, email, password, expected",
    [
        ("Ua",
         Data.USER_EMAIL,
         INVALID_PASSWORD_ERROR_UA),
        ("En",
         Data.USER_EMAIL,
         INVALID_PASSWORD_ERROR_EN),
    ],
    indirect=["setup_function"]
)
def test_verify_error_message_for_invalid_password(email,
                                                   expected,
                                                   setup_function):
    """
    This test checks the correctness of error messages when entering a randomly generated invalid password
    on login pages with different language settings (Ukrainian and English).

    Parameters:
    - email: The user's email.
    - expected: The expected error message for invalid password.
    """
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    login_form = setup_function

    with allure.step("Enter email and password"):
        login_form.enter_email(email).enter_password(password)

    with allure.step("Click sign in and get error message"):
        actual = (login_form
                  .click_sign_in_button()
                  .password
                  .get_error_message())

    with allure.step("Verify error message"):
        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
