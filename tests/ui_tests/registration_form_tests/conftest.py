import pytest
from playwright.sync_api import sync_playwright

from modules.constants import Data
from modules.localization_utils import LocalizationUtils
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="function")
def registration_form_setup(request):
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


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def initialize_page(playwright_instance, request):
    browser = playwright_instance.chromium.launch(
        headless=False
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    language = request.config.getoption("--language", default="Ua")
    localization_utils = LocalizationUtils(language=language)
    page.goto(f"{Data.UI_BASE_URL}greenCity")

    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    yield home_page, localization_utils
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def registration_form_field_setup(initialize_page):
    home_page, localization_utils = initialize_page
    form = home_page.header_component.open_registration_form()
    yield form, localization_utils
    form.close()
