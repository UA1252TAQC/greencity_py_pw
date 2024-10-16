import allure
from playwright.sync_api import Page


class EmailField:
    def __init__(self, page: Page):
        self.page = page
        self.input_selector = "input#email"
        self.error_selector = ".error-message, .error-message-show, .alert-general-error, .validation-email-error"

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

    @allure.step("Check, if Email field is empty")
    def is_email_field_empty(self) -> bool:
        return "ng-pristine" in self.page.locator("input#email").get_attribute("class")
