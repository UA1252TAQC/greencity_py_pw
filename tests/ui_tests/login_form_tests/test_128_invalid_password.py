import pytest
from faker.contrib.pytest.plugin import faker

from modules.constants import Data
from faker import Faker

fake = Faker()

INVALID_PASSWORD_ERROR_UA = "Введено невірний email або пароль."
INVALID_PASSWORD_ERROR_EN = "Bad email or password."


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

    actual = (login_form
              .enter_email(email)
              .enter_password(password)
              .click_sign_in_button()
              .password
              .get_error_message())

    assert actual == expected, f"Expected '{expected}', but got '{actual}'"
