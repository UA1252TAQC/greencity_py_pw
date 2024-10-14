import pytest

from playwright.sync_api import sync_playwright
from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="session")
def playwright_instance():
    """
        This fixture initializes the Playwright instance for the entire test session.
        It launches Playwright and keeps it running throughout all tests.
        At the end of the session, Playwright is stopped.
        """
    p = sync_playwright().start()
    yield p
    p.stop()


@pytest.fixture(scope="function")
def initialize_page(playwright_instance):
    """
        This fixture initializes the browser, opens a new context and page for each test.
        It navigates to the GreenCity homepage and adjusts the viewport settings.

        Returns:
        - home_page: An instance of the GreenCityHomePage class.

        After the test is complete, the browser context and page are closed.
        """
    browser = playwright_instance.chromium.launch(
        headless=False
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080, "device_scale_factor": 1})
    page = context.new_page()
    page.goto(f"{Data.UI_BASE_URL}/#/greenCity", wait_until="load")
    page.evaluate("() => document.body.style.zoom='100%'")

    home_page = GreenCityHomePage(page)
    yield home_page
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def setup_function(initialize_page, language):
    """
    This fixture sets the language on the GreenCity homepage and opens the login form.

    Parameters:
    - initialize_page: The fixture that initializes the GreenCity homepage.
    - language: The language parameter passed to set the page language.

    Returns:
    - form: The opened login form.

    The form is closed after the test is complete.
    """
    home_page = initialize_page
    home_page.header_component.set_language(language)
    form = home_page.header_component.open_login_form()
    yield form
    form.close()
