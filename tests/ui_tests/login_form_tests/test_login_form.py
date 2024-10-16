import pytest
import allure
from modules.constants import Data
from ui.constants.Colors import Colors


@allure.description("Verify that the 'Sign in' button is remained inactive after leaving the fields empty")
@allure.feature("Login")
@allure.issue("https://github.com/UA1252TAQC/GreenCityTAJava/issues/64", "64")
def test_signin_btn_is_inactive_by_empty_fields(initialize_page):
    login_modal_component = initialize_page \
        .header_component \
        .open_login_form()
    assert login_modal_component.email.is_email_field_empty()
    assert login_modal_component.password.is_password_field_empty()
    assert not login_modal_component.is_signin_btn_active()


@allure.description("Verify that the ‘Sign in’ button is activeted and highlighted in green after entering "
                    "a valid email and password")
@allure.feature("Login")
@allure.issue("https://github.com/UA1252TAQC/GreenCityTAJava/issues/61", "61")
def test_signin_btn_becomes_green_by_valid_creds(initialize_page):
    login_modal_component = initialize_page.header_component.open_login_form()
    assert not login_modal_component.is_signin_btn_active()
    login_modal_component.enter_email(Data.USER_EMAIL).enter_password(Data.USER_PASSWORD)
    assert login_modal_component.is_signin_btn_active()
    assert login_modal_component.is_highlighted_signin_btn_in_color(Colors.PRIMARY_DARK_GREEN)


@allure.description("Verify that user is navigated to the Google register page after clicking the "
                    "'Sign in with Google' button on the sign-in page")
@allure.feature("Login")
@allure.issue("https://github.com/UA1252TAQC/GreenCityTAJava/issues/73", "73")
def test_link_signin_with_google(initialize_page):
    google_auth_component = initialize_page.header_component \
        .open_login_form() \
        .click_signin_with_google_btn()
    assert "accounts.google.com" in google_auth_component.page.url, "Wrong URL"
    assert google_auth_component.is_email_input_displayed, "There is no element after following link"


@allure.description("Verify that the message \"{expected_message}\" is shown below the 'Email' field "
                    "after click recover the password")
@allure.feature("Forgot Password")
@allure.issue("https://github.com/UA1252TAQC/GreenCityTAJava/issues/71", "71")
@pytest.mark.parametrize("language, expected_message", [
    ("EN", "Password restore link already sent, please check your email: "),
    ("UA", "Посилання на відновлення пароля вже надіслано, перевірте свою електронну адресу: ")
])
def test_message_after_recover_pass(initialize_page, language, expected_message):
    home_page = initialize_page.header_component
    home_page.set_language(language)
    home_page.open_login_form() \
        .click_forgot_password_link() \
        .enter_email(Data.USER_EMAIL) \
        .click_submit_login_link()

    initialize_page.reload_page()
    home_page = initialize_page.header_component
    home_page.set_language(language)
    hint_message = home_page.open_login_form() \
        .click_forgot_password_link() \
        .enter_email(Data.USER_EMAIL) \
        .click_submit_login_link() \
        .get_hint_message()
    assert hint_message == expected_message + Data.USER_EMAIL
