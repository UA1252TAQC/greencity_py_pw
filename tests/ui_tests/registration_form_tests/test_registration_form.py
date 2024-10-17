import pytest
import allure
import logging as log

from modules.constants import Data
from modules.dataprovider_utils import DataProvider
from modules.mail_utils import MailUtils
from ui.pages.green_city.green_city_home_page import GreenCityHomePage
from ui.pages.green_city.profile_page import ProfilePage
from ui.pages.ubs.ubs_home_page import UbsHomePage


@allure.title("Verify pop-up sign-up validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form pop-up sign-up validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_registration_success_message, expected_account_submit_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testPopUpSignUpValidation"),
)
def test_pop_up_sign_up_validation(expected_registration_success_message, expected_account_submit_message,
                                   mail_box, username, password, repeat_password, registration_form_setup):
    log.info("Starting test_pop_up_sign_up_validation with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    form = home_page.header_component.open_registration_form()

    form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()
    actual_registration_success_message = home_page.get_pop_up_message()
    log.info("Registration success message: %s", actual_registration_success_message)
    assert actual_registration_success_message == localization_utils.get_form_message(expected_registration_success_message)

    mail = MailUtils().get_last_mail(mail_box["id"])
    home_page.open_url_in_new_tab(MailUtils.extract_activation_link(mail["body"]))

    ubs_page = UbsHomePage(home_page.page)
    actual_account_submit_message = ubs_page.get_pop_up_message()
    log.info("Account submit message: %s", actual_account_submit_message)
    assert actual_account_submit_message == localization_utils.get_form_message(expected_account_submit_message)


@allure.title("Verify Google sign-up process")
@allure.description("""
    This test validates the Google sign-up process for unregistered users on the Green City application.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Google sign-up process validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "google_email, google_password, expected_google_name",
    DataProvider.get_ui_test_data("testGoogleSignUp"),
)
def test_google_sign_up(
        google_email,
        google_password,
        expected_google_name,
        registration_form_setup
):
    log.info("Starting test_google_sign_up with Google email: %s", google_email)
    page, _, _ = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    form = home_page.header_component.open_registration_form()

    google_form = form.open_auth_google_form()
    google_form.enter_email(google_email).click_email_submit_button().enter_password(
        google_password).click_password_submit_button()

    home_page.switch_to_active_tab()
    profile_page = ProfilePage(home_page.page)

    auth_token = profile_page.get_auth_token()
    log.info("Auth token: %s", auth_token)
    assert auth_token is not None, (
        "Validating that the JWT token is not null after Google sign-up."
    )
    username = profile_page.header_component.get_username()
    log.info("Google account name: %s", username)
    assert username == expected_google_name, (
        "Validating that the Google account name matches the expected name."
    )


@allure.title(
    "Verify error message for already registered in Green City user without confirm the email during UBS sign-up")
@allure.description("""
This test checks the scenario where a user registered from the Green City site,
but hasn't confirmed their email yet, tries to register again from the UBS site.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testRegisteredGreenCity"),
)
def test_registered_green_city(
        expected_registration_error_message,
        mail_box,
        username,
        password,
        repeat_password,
        registration_form_setup
):
    log.info("Starting test_registered_green_city with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    home_page.open_url_in_new_tab(f"{Data.UI_BASE_URL}ubs")
    ubs_page = UbsHomePage(home_page.page)
    ubs_page.header_component.set_language(language)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_registration_error_message = ubs_form.email.get_error_message()
    log.info("Registration error message: %s", actual_registration_error_message)
    assert actual_registration_error_message == localization_utils.get_form_message(
        expected_registration_error_message), (
        "Validating the error message for already registered email."
    )


@allure.title(
    "Verify error message for already registered in UBS user without confirm the email during Green City sign-up")
@allure.description("""
    This test checks the scenario where a user registered from the UBS site,
    but hasn't confirmed their email yet, tries to register again from the Green City site.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testRegisteredUbs"),
)
def test_registered_ubs(
        expected_registration_error_message,
        mail_box,
        username,
        password,
        repeat_password,
        registration_form_setup
):
    log.info("Starting test_registered_ubs with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}ubs")
    ubs_page = UbsHomePage(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    ubs_page.open_url_in_new_tab(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(ubs_page.page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_registration_error_message = home_form.email.get_error_message()
    log.info("Registration error message: %s", actual_registration_error_message)
    assert actual_registration_error_message == localization_utils.get_form_message(
        expected_registration_error_message), (
        "Validating the error message for already registered email in UBS."
    )


@allure.title("Verify error message for already registered email")
@allure.description("""
    This test verifies that when a user attempts to register with an email that is
    already registered on the Green City platform, the appropriate error message  is displayed.""")
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testEmailAlreadyExists"),
)
def test_email_already_exists(
        expected_registration_error_message,
        mail_box,
        username,
        password,
        repeat_password,
        registration_form_setup
):
    log.info("Starting test_email_already_exists with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_error_message = home_form.email.get_error_message()
    log.info("Error message: %s", actual_error_message)
    assert actual_error_message == localization_utils.get_form_message(expected_registration_error_message), (
        "Validating the error message for already registered email."
    )


@allure.title("Verify error message for already registered email from Green City with confirm the email on UBS sign-up")
@allure.description("""
    This test validates that a user who has already registered from the Green City site with confirm
    the email and tries to sign up on the UBS site receives the appropriate error message.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testGreenCityRegisteredWithConfirmEmail"),
)
def test_green_city_registered_with_confirm_email(
        expected_error_message,
        mail_box,
        username,
        password,
        repeat_password,
        registration_form_setup
):
    log.info("Starting test_green_city_registered_with_confirm_email with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    mail = MailUtils().get_last_mail(mail_box["id"])
    home_page.open_url_in_new_tab(MailUtils.extract_activation_link(mail["body"]))

    home_page.open_url_in_new_tab(f"{Data.UI_BASE_URL}ubs")
    ubs_page = UbsHomePage(home_page.page)
    ubs_page.header_component.set_language(language)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_registration_error_message = ubs_form.email.get_error_message()
    log.info("Registration error message: %s", actual_registration_error_message)
    assert actual_registration_error_message == localization_utils.get_form_message(expected_error_message)


@allure.title("Verify error message for already registered email from UBS with confirm the email on Green City sign-up")
@allure.description("""
    This test validates that a user who has already registered from the UBS site with confirm
    the email and tries to sign up on the Green City site receives the appropriate error message.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "expected_registration_error_message, mail_box, username, password, repeat_password",
    DataProvider.get_ui_test_data("testUbsRegisteredWithConfirmEmail"),
)
def test_ubs_registered_with_confirm_email(
        expected_registration_error_message,
        mail_box,
        username,
        password,
        repeat_password,
        registration_form_setup
):
    log.info("Starting test_ubs_registered_with_confirm_email with username: %s", username)
    page, localization_utils, language = registration_form_setup
    page.goto(f"{Data.UI_BASE_URL}ubs")
    ubs_page = UbsHomePage(page)
    ubs_form = ubs_page.header_component.open_registration_form()
    ubs_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    mail = MailUtils().get_last_mail(mail_box["id"])
    ubs_page.open_url_in_new_tab(MailUtils.extract_activation_link(mail["body"]))

    ubs_page.open_url_in_new_tab(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(ubs_page.page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_registration_error_message = home_form.email.get_error_message()
    log.info("Registration error message: %s", actual_registration_error_message)
    assert actual_registration_error_message == localization_utils.get_form_message(
        expected_registration_error_message), (
        "Validating the error message for already registered email in Green City."
    )
