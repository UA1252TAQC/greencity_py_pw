from playwright.sync_api import Page

from ui.components.green_city_header_component import GreenCityHeaderComponent


class GreenCityHomePage:
    def __init__(self, page: Page):
        self.d = 123
        self.page = page
        self.header_component = GreenCityHeaderComponent(page)

    def set_language(self, language: str):
        self.page.click(f"//button[@data-language='{language}']")
        return self
