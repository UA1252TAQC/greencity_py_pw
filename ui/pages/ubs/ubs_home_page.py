from playwright.sync_api import Page

from ui.pages.ubs.base_page_ubs import BasePageUbs


class UbsHomePage(BasePageUbs):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page.wait_for_selector("//header[@role='banner']", timeout=20000)

    def set_language(self, language: str):
        self.get_header_component().set_language(language)
        return self
