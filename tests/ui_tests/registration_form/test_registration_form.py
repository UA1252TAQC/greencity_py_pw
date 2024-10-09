from playwright.sync_api import Page
import pytest

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="function", autouse=True)
def setup(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto(f"{Data.UI_BASE_URL}greenCity")


def test_pop_up_sign_up_validation(page):
    home_page = GreenCityHomePage(page)
    form = home_page.header_component.open_registration_form()
    form.fill_form("mail_box.address", "username", "password", "repeat_password").submit()
