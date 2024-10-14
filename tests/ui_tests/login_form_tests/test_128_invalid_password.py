import pytest

from modules.constants import Data

INVALID_PASSWORD_ERROR_UA = "Введено невірний email або пароль."
INVALID_PASSWORD_ERROR_EN = "Bad email or password."


@pytest.mark.parametrize(
    "language, email, password, expected",
    [
        ("Ua", Data.USER_EMAIL, Data.USER_PASSWORD + "@123", INVALID_PASSWORD_ERROR_UA),
        ("En", Data.USER_EMAIL, Data.USER_PASSWORD + "@123", INVALID_PASSWORD_ERROR_EN),
    ],
    indirect=["setup_function"]
)
def test_verify_error_message_for_invalid_password(email,
                                                   password,
                                                   expected,
                                                   setup_function):
    """
        This test checks the correctness of error messages when entering an invalid password
        on login pages with different language settings (Ukrainian and English).

        Parameters:
        - email: The user's email.
        - password: The incorrect password to test.
        - expected: The expected error message.
        """
    login_form = setup_function

    actual = (login_form
              .enter_email(email)
              .enter_password(password)
              .click_sign_in_button()
              .password
              .get_error_message())

    assert actual == expected, f"Expected '{expected}', but got '{actual}'"
