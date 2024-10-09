from playwright.sync_api import Page, expect
from time import sleep


class Base:
    DURATION_FIVE_SECOND = 5
    DURATION_TEN_SECOND = 10

    def __init__(self, page: Page):
        self.page = page

    def get_actions(self):
        return self.page.mouse

    def get_wait(self, seconds: int):
        return self.page.wait_for_timeout(seconds * 1000)

    def sleep(self, seconds: int):
        sleep(seconds)

    def get_text(self, element):
        return element.inner_text()

    def find_with_wait_element(self, selector: str, seconds: int):
        self.page.wait_for_selector(selector, timeout=seconds * 1000)
        return self.page.locator(selector)

    def wait_staleness_of(self, selector: str):
        element = self.page.locator(selector)
        if element.count() > 0:
            self.page.wait_for_timeout(self.DURATION_FIVE_SECOND * 1000)
            expect(element).to_be_hidden()

    def click(self, element):
        element.click()

    def clear(self, element):
        element.fill("")

    def is_displayed(self, element):
        try:
            return element.is_visible()
        except Exception:
            return False

    def is_enabled(self, element):
        if not self.is_displayed(element):
            return False
        return element.is_enabled()

    def is_present(self, selector: str):
        return self.page.locator(selector).count() > 0
