from playwright.sync_api import Page
import pytest

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.fixture(scope="function")
def setup(page: Page):
    page.goto(f"{Data.UI_BASE_URL}greenCity")
    return GreenCityHomePage(page)


def test_pop_up_sign_up_validation(setup):
    home_page = setup
    print(1234)

    form = home_page.header_component.open_registration_form()
    form.fill_form("mail_box.address", "username", "password", "repeat_password").submit()


# def test_pop_up_sign_up():
#     print(12345)


# class GreenCityHomePage1:
#     def __init__(self, page: Page):
#         self.page = page
#         # self.header_component = GreenCityHeaderComponent(page)

#     def set_language(self, language: str):
#         self.page.click(f"//button[@data-language='{language}']")
#         return self
