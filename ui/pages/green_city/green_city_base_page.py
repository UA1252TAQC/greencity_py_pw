from playwright.sync_api import Page

from ui.components.green_city_header_component import GreenCityHeaderComponent
from ui.pages.base_page import BasePage


class GreenCityBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header_component = GreenCityHeaderComponent(page)
