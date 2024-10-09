from playwright.sync_api import Page

from ui.components.ubs_header_component import UbsHeaderComponent
from ui.pages.base_page import BasePage


class UbsBasePage(BasePage):
    def __init__(self, page: Page):
        self.page = page
        self.header_component = UbsHeaderComponent(page)
