from playwright.sync_api import Page

from ui.pages.ubs.ubs_base_page import UbsBasePage


class UbsHomePage(UbsBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
