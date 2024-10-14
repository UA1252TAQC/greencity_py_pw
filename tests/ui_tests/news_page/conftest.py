import pytest
from playwright.sync_api import sync_playwright

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="function")
def setup_function():
    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(f"{Data.UI_BASE_URL}/#/greenCity")
        home_page = GreenCityHomePage(page)

        home_page.header_component.set_language('en')
        home_page.header_component.open_login_form() \
            .fill_form(Data.USER_EMAIL, Data.USER_PASSWORD) \
            .click_sign_in_button_and_successful_login() \
            .header_component.open_news_link() \
            .click_create_news(page)

        yield page

        context.close()
        browser.close()
