from playwright.sync_api import Page

from ui.components.ubs_header_component import UbsHeaderComponent
from ui.pages.base_page import BasePage


class BasePageUbs(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def get_header_component(self):
        return UbsHeaderComponent(self.page)
