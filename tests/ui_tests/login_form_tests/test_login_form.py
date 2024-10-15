import pytest
from playwright.sync_api import sync_playwright
import allure

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="function")
def setup_function(request):
    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(
            headless=False
        )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        yield page

        context.close()
        browser.close()


def test_successful_sign_in(setup_function):
    page = setup_function
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity")
    profile_page = (GreenCityHomePage(page)
                    .header_component.open_login_form()
                    .enter_email(Data.USER_EMAIL)
                    .enter_password(Data.USER_PASSWORD)
                    .click_sign_in_button_and_successful_login())

    assert profile_page.page.url == f"{Data.UI_BASE_URL}/#/profile/{Data.USER_ID}"
    assert profile_page.header_component.get_username() == Data.USER_NAME


@allure.description("Verify that the 'Sign in' button is remained inactive after leaving the fields empty")
@allure.feature("Login")
@allure.issue("64")
def test_signin_btn_is_inactive_by_empty_fields(setup_function):
    page = setup_function
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity")
    login_modal_component = (GreenCityHomePage(page)
                             .header_component
                             .open_login_form())
    assert login_modal_component.email.is_email_field_empty()
    assert login_modal_component.password.is_password_field_empty()
    assert not login_modal_component.is_signin_btn_active()


@allure.description("Verify that the ‘Sign in’ button is activeted and highlighted in green after entering "
                    "a valid email and password")
@allure.feature("Login")
@allure.issue("61")
def test_signin_btn_becomes_green_by_valid_creds(setup_function):
    page = setup_function
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity")
    login_modal_component = GreenCityHomePage(page).header_component.open_login_form()
    assert not login_modal_component.is_signin_btn_active()
    login_modal_component.enter_email(Data.USER_EMAIL).enter_password(Data.USER_PASSWORD)
    assert login_modal_component.is_signin_btn_active()
    assert login_modal_component.is_highlighted_signin_btn_in_color("rgb(19, 170, 87)")


@allure.description("Verify that user is navigated to the Google register page after clicking the "
                    "'Sign in with Google' button on the sign-in page")
@allure.feature("Login")
@allure.issue("73")
def test_link_signin_with_google(setup_function):
    page = setup_function
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity")
    google_auth_component: page = (GreenCityHomePage(page)
                                   .header_component.open_login_form()
                                   .click_signin_with_google_btn())
    assert "accounts.google.com" in google_auth_component.page.url, "Wrong URL"
    assert google_auth_component.is_email_input_displayed, "There is no element after following link"
