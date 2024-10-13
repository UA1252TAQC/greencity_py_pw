import pytest
from playwright.sync_api import sync_playwright

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


def test_verify_error_message_for_invalid_password(setup_function):
    page = setup_function
    page = setup_function
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity")

    (GreenCityHomePage(page)
     .header_component
     .set_language('en'))

    (GreenCityHomePage(page)
     .header_component
     .open_login_form()
     .enter_email('wodepab265@craftapk.com')
     .enter_password('djsfskdfksd')
     .click_sign_in_button())
