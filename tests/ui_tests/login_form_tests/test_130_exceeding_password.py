import allure
import pytest
from faker import Faker

from modules.constants import Data

fake = Faker()

EXCEEDING_PASSWORD_ERROR_UA = "Пароль повинен містити менше 20 символів без пробілів."
EXCEEDING_PASSWORD_ERROR_EN = "Password must be less than 20 characters long without spaces."


@allure.title("Verify Error Message for exceeding password")
@allure.description("This test checks the validation of the login form fields.")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Login form")
@allure.issue("130")
@pytest.mark.parametrize(
    "language, email, expected",
    [
        ("Ua",
         Data.USER_EMAIL,
         EXCEEDING_PASSWORD_ERROR_UA),
        ("En",
         Data.USER_EMAIL,
         EXCEEDING_PASSWORD_ERROR_EN),
    ]
)
def test_verify_error_message_for_exceeding_password(language, email, expected, setup_function):
    """
       This test verifies the error message displayed when a user attempts to log in
       with an empty email and/or password field in the login form.

       Parameters:
       - email: The email address to enter in the login form (can be empty).
       - password: The password to enter in the login form (can be empty).
       - expected: The expected error message when one or both fields are left empty.
       - setup_function: Fixture that initializes the login form and sets up the environment for the test.
       """
    password = fake.password(length=30, special_chars=True, digits=True, upper_case=True, lower_case=True)

    login_form = setup_function

    with (allure.step("Enter email and password")):
        (login_form
         .enter_email(email)
         .enter_password(password))

    with allure.step("Click outside the form and get error message"):
        actual = (login_form
                  .click_outside_form()
                  .password
                  .get_error_message())

    with allure.step("Verify error message"):
        assert actual == expected, f"Expected '{expected}', but got '{actual}'"
