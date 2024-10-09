from playwright.sync_api import Page
from ui.components.green_city_header_component import GreenCityHeaderComponent


class BasePageGreenCity:
    def __init__(self, page: Page):
        self.page = page

    def get_header_component(self):
        return GreenCityHeaderComponent(self.page, self.header_root_element)
