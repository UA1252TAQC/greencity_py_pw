import pytest
from playwright.sync_api import sync_playwright

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage
from ui.pages.green_city.green_city_profile_page import GreenCityProfilePage


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
    login_modal = GreenCityHomePage(page).header_component.open_login_form()
    login_modal.enter_email(Data.USER_EMAIL)
    login_modal.enter_password(Data.USER_PASSWORD)
    login_modal.click_sign_in_button_and_successful_login()

    profile_page = GreenCityProfilePage(page)

    assert profile_page.page.url == f"{Data.UI_BASE_URL}/#/profile/{Data.USER_ID}"
    assert profile_page.header_component.get_username() == Data.USER_NAME
