from playwright.sync_api import Page

from ui.pages.green_city.green_city_base_page import GreenCityBasePage


class GreenCityHomePage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
