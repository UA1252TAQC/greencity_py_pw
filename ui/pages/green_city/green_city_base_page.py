from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class GreenCityBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        from ui.components.green_city_header_component import GreenCityHeaderComponent
        self.header_component = GreenCityHeaderComponent(page)
