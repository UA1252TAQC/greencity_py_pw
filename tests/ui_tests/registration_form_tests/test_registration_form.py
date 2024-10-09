import base64
import json
from datetime import timedelta

import allure
from playwright.sync_api import Page
import pytest

from modules.constants import Data
from modules.dataprovider import DataProvider
from modules.jwt_payload import JwtPayload
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


# @pytest.fixture(scope="function", autouse=True)
# def setup(page: Page):
#     page.set_viewport_size({"width": 1920, "height": 1080})
#     page.goto(f"{Data.UI_BASE_URL}greenCity")
#
#
# def test_pop_up_sign_up_validation(page):
#     home_page = GreenCityHomePage(page)
#     form = home_page.header_component.open_registration_form()
#     form.fill_form("mail_box.address", "username", "password", "repeat_password").submit()

@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"{Data.UI_BASE_URL}greenCity")


def parse_jwt(token: str) -> JwtPayload:
    if not token:
        return None
    parts = token.split(".")
    payload = parts[1]
    decoded_bytes = base64.urlsafe_b64decode(payload + '==')
    decoded_payload = decoded_bytes.decode('utf-8')
    return JwtPayload(**json.loads(decoded_payload))


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_account_submit_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testPopUpSignUpValidation"),
)
@allure.description("Tests the validation of the pop-up sign-up process.")
@allure.feature("Registration")
@allure.issue("12")
def test_pop_up_sign_up_validation(page: Page, expected_registration_success_message, expected_account_submit_message,
                                   mail_box: MailBoxCredentials, username, password, repeat_password):
    home_page = GreenCityHomePage(page)
    form = home_page.header_component.open_registration_form()
    form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = home_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message, "Validating the success message after registration."

    mail = Mail.get_last_email(mail_box.id)
    home_page.open_url_in_new_tab(mail.extract_activation_link())
    ubs_page = HomePageUbs(page)

    actual_account_submit_message = ubs_page.get_pop_up_message()
    assert actual_account_submit_message == expected_account_submit_message, "Validating the account submission message after activation."

    login_form = ubs_page.header_component.get_current_login_form()
    profile_page = login_form.fill_form(mail_box.address, password).click_sign_in_button_successful_login()

    jwt_payload = parse_jwt(profile_page.get_auth_token())
    assert jwt_payload.exp == jwt_payload.iat + timedelta(
        hours=24), "Validating the JWT token expiration time is 24 hours."


@pytest.mark.parametrize(
    "google_email, google_password, expected_google_name",
    DataProvider.get_ui_test_data("testGoogleSignUp"),
)
@allure.description("Tests the Google sign-up process.")
@allure.feature("Registration")
@allure.issue("13")
def test_google_sign_up(page: Page, google_email, google_password, expected_google_name):
    home_page = GreenCityHomePage(page)
    form = home_page.header_component.open_registration_form()

    google_form = form.open_auth_google_form()
    google_form.enter_email(google_email).click_email_submit_button().enter_password(
        google_password).click_password_submit_button()

    home_page.switch_to_active_tab()
    profile_page = ProfilePage(page)

    assert profile_page.get_auth_token() is not None, "Validating that the JWT token is not null after Google sign-up."
    assert page.url.startswith(
        f"{Data.UI_BASE_URL}/#/profile"), "Validating that the user is redirected to the profile page."
    assert profile_page.header_component.get_username() == expected_google_name, "Validating that the Google account name matches the expected name."


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testRegisteredGreenCity"),
)
@allure.description("Tests registration with already existing Green City account.")
@allure.feature("Registration")
@allure.issue("12")
def test_registered_green_city(page: Page, expected_registration_success_message, expected_registration_error_message,
                               mail_box: MailBoxCredentials, username, password, repeat_password):
    home_page = GreenCityHomePage(page)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = home_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message, "Validating the success message after registration."

    ubs_page = HomePageUbs(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_error_message = ubs_form.get_email().get_error_message()
    assert actual_registration_error_message == expected_registration_error_message, "Validating the error message for already registered email."


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testRegisteredUbs"),
)
@allure.description("Tests registration with an already existing UBS account.")
@allure.feature("Registration")
@allure.issue("12")
def test_registered_ubs(page: Page, expected_registration_success_message, expected_registration_error_message,
                        mail_box: MailBoxCredentials, username, password, repeat_password):
    ubs_page = HomePageUbs(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = ubs_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message, "Validating the success message after registration."

    home_page = GreenCityHomePage(page)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_error_message = home_form.get_email().get_error_message()
    assert actual_registration_error_message == expected_registration_error_message, "Validating the error message for already registered email in UBS."


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testEmailAlreadyExists"),
)
@allure.description("Tests the behavior when attempting to register with an already existing email.")
@allure.feature("Registration")
@allure.issue("12")
def test_email_already_exists(page: Page, expected_registration_success_message, expected_registration_error_message,
                              mail_box: MailBoxCredentials, username, password, repeat_password):
    home_page = GreenCityHomePage(page)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = home_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message, "Validating the success message after registration."

    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_error_message = home_form.get_email().get_error_message()
    assert actual_error_message == expected_registration_error_message, "Validating the error message for already registered email."


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_account_submit_message, expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testGreenCityRegisteredWithConfirmEmail"),
)
@allure.description("Tests the registration process when confirming an email for a Green City account.")
@allure.feature("Registration")
@allure.issue("12")
def test_green_city_registered_with_confirm_email(page: Page, expected_registration_success_message,
                                                  expected_account_submit_message, expected_registration_error_message,
                                                  mail_box: MailBoxCredentials, username, password, repeat_password):
    home_page = GreenCityHomePage(page)
    green_city_form = home_page.header_component.open_registration_form()
    green_city_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = home_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message, "Validating the success message after registration."

    mail = Mail.get_last_email(mail_box.id)
    home_page.open_url_in_new_tab(mail.extract_activation_link())

    actual_account_submit_message = home_page.get_pop_up_message()
    assert actual_account_submit_message == expected_account_submit_message

    ubs_page = HomePageUbs(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_error_message = ubs_form.get_email().get_error_message()
    assert actual_registration_error_message == expected_registration_error_message


@pytest.mark.parametrize(
    "expected_registration_success_message, expected_account_submit_message, expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testUbsRegisteredWithConfirmEmail"),
)
@allure.description("Tests the registration process when confirming an email for a UBS account.")
@allure.feature("Registration")
@allure.issue("12")
def test_ubs_registered_with_confirm_email(page: Page, expected_registration_success_message,
                                           expected_account_submit_message, expected_registration_error_message,
                                           mail_box: MailBoxCredentials, username, password, repeat_password):
    ubs_page = HomePageUbs(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_success_message = ubs_page.get_pop_up_message()
    assert actual_registration_success_message == expected_registration_success_message

    mail = Mail.get_last_email(mail_box.id)
    ubs_page.open_url_in_new_tab(mail.extract_activation_link())

    actual_account_submit_message = ubs_page.get_pop_up_message()
    assert actual_account_submit_message == expected_account_submit_message, "Validating the account submission message after email confirmation."

    home_page = GreenCityHomePage(page)
    green_city_form = home_page.header_component.open_registration_form()
    green_city_form.fill_form(mail_box.address, username, password, repeat_password).submit()

    actual_registration_error_message = green_city_form.get_email().get_error_message()
    assert actual_registration_error_message == expected_registration_error_message, "Validating the error message for already registered email in Green City."