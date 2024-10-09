from playwright.sync_api import Page
from ui.components.green_city_header_component import GreenCityHeaderComponent
from ui.pages.base_page import BasePage


class BasePageGreenCity(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_header_component(self):
        return GreenCityHeaderComponent(self.page, self.header_root_element)
