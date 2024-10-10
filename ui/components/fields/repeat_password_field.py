from playwright.sync_api import Page


class RepeatPasswordField:
    def __init__(self, page: Page):
        self.page = page
        self.input_selector = "input#repeatPassword"
        self.error_selector = "#confirm-err-msg div"

    def enter(self, text: str):
        if text is not None:
            self.page.fill(self.input_selector, text)

    def is_displayed(self) -> bool:
        return self.page.is_visible(self.input_selector)

    def get_error_message(self):
        if self.page.is_visible(self.error_selector):
            return self.page.inner_text(self.error_selector)
        return None

    def is_valid(self) -> bool:
        return not self.page.is_visible(self.error_selector)

    def clear(self):
        self.page.click(self.input_selector)
        self.page.fill(self.input_selector, "")
