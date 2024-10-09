from playwright.sync_api import Page


class UsernameField:
    def __init__(self, page: Page):
        self.page = page

    def enter(self, text: str):
        if text:
            self.page.fill("input#firstName", text)

    def is_displayed(self) -> bool:
        return self.page.is_visible("input#firstName")

    def get_error_message(self) -> str:
        error_selector = "#firstname-err-msg div"
        if self.page.is_visible(error_selector):
            return self.page.inner_text(error_selector)
        return None

    def is_valid(self) -> bool:
        error_selector = "#firstname-err-msg div"
        return not self.page.is_visible(error_selector)

    def clear(self):
        self.page.click("input#firstName")
        self.page.fill("input#firstName", "")
