from playwright.sync_api import sync_playwright
import pytest
import allure

from modules.constants import Data
from modules.dataprovider import DataProvider
from modules.localization_utils import LocalizationUtils
from modules.mail_utils import MailUtils
from ui.pages.green_city.green_city_home_page import GreenCityHomePage
from ui.pages.green_city.profile_page import ProfilePage
from ui.pages.ubs.ubs_home_page import UbsHomePage


@pytest.fixture(scope="function")
def setup_function(request):
    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(
            headless=False
        )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        language = request.config.getoption("--language", default="Ua")
        localization_utils = LocalizationUtils(language=language)

        yield page, localization_utils, language
        context.close()
        browser.close()

# TODO EXTRACT


# def parse_jwt(token: str) -> JwtPayload:
#     if not token:
#         return None
#     parts = token.split(".")
#     payload = parts[1]
#     decoded_bytes = base64.urlsafe_b64decode(payload + '==')
#     decoded_payload = decoded_bytes.decode('utf-8')
#     return JwtPayload(**json.loads(decoded_payload))

# # TODO FIX
# @allure.title("Verify registration email field validation")
# @allure.description("""
#     This test checks the validation of the registration form fields.
#                     """)
# @allure.severity(allure.severity_level.NORMAL)
# @allure.epic("Green City")
# @allure.feature("Registration form")
# @allure.story("Registration form email field validation")
# @allure.tag("Green City")
# @allure.issue("12")
# @pytest.mark.parametrize(
#     "expected_registration_success_message, expected_account_submit_message, mail_box, username, password, repeat_password",
#     DataProvider.get_ui_test_data("testPopUpSignUpValidation"),
# )
# def test_pop_up_sign_up_validation(expected_registration_success_message, expected_account_submit_message,
#                                    mail_box, username, password, repeat_password, setup_function):
#     page, localization_utils, language = setup_function
#     page.goto(f"{Data.UI_BASE_URL}greenCity")
#     home_page = GreenCityHomePage(page)
#     home_page.header_component.set_language(language)
#     form = home_page.header_component.open_registration_form()
#     form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

#     mail = MailUtils().get_last_mail(mail_box["id"])
#     home_page.open_url_in_new_tab(MailUtils.extract_activation_link(mail["body"]))

#  WAIT FOR LOGIN COMPONENT
#     ubs_page = UbsHomePage(home_page.page)

    # login_form = ubs_page.header_component.get_current_login_form()
    # profile_page = login_form.fill_form(mail_box["emailAddress"], password).click_sign_in_button_successful_login()

    # jwt_payload = parse_jwt(profile_page.get_auth_token())
    # assert jwt_payload.exp == jwt_payload.iat + timedelta(
    #     hours=24), "Validating the JWT token expiration time is 24 hours."

@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
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
    setup_function
):
    page, _, _ = setup_function
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    form = home_page.header_component.open_registration_form()

    google_form = form.open_auth_google_form()
    google_form.enter_email(google_email).click_email_submit_button().enter_password(
        google_password).click_password_submit_button()

    home_page.switch_to_active_tab()
    profile_page = ProfilePage(home_page.page)

    assert profile_page.get_auth_token() is not None, (
        "Validating that the JWT token is not null after Google sign-up."
    )
    assert profile_page.header_component.get_username() == expected_google_name, (
        "Validating that the Google account name matches the expected name."
    )


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
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
    setup_function
):
    page, localization_utils, language = setup_function
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
    assert actual_registration_error_message == localization_utils.get_form_message(expected_registration_error_message), (
        "Validating the error message for already registered email."
    )


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
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
    setup_function
):
    page, localization_utils, language = setup_function
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
    assert actual_registration_error_message == localization_utils.get_form_message(expected_registration_error_message), (
        "Validating the error message for already registered email in UBS."
    )


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
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
    setup_function
):
    page, localization_utils, language = setup_function
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    home_form = home_page.header_component.open_registration_form()
    home_form.fill_form(mail_box["emailAddress"], username, password, repeat_password).submit()

    actual_error_message = home_form.email.get_error_message()
    assert actual_error_message == localization_utils.get_form_message(expected_registration_error_message), (
        "Validating the error message for already registered email."
    )


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
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
    setup_function
):
    page, localization_utils, language = setup_function
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
    assert actual_registration_error_message == localization_utils.get_form_message(expected_error_message)


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
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
    setup_function
):
    page, localization_utils, language = setup_function
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
    assert actual_registration_error_message == localization_utils.get_form_message(expected_registration_error_message), (
        "Validating the error message for already registered email in Green City."
    )
