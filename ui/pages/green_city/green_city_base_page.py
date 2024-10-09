from playwright.sync_api import Page

from ui.components.green_city_header_component import GreenCityHeaderComponent


class GreenCityBasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header_component = GreenCityHeaderComponent(page)
