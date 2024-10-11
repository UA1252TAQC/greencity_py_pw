from playwright.sync_api import Page

from ui.pages.green_city.green_city_base_page import GreenCityBasePage


class CreateNewsPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super(page).__init__(page)
