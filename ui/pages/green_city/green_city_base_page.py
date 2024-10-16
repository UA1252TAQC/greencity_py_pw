from playwright.sync_api import Page
from ui.pages.base_page import BasePage
from ui.components.component_factory import create_green_city_header_component


class GreenCityBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header_component = create_green_city_header_component(page)
