from playwright.sync_api import Page
import allure


class EmailField:
    def __init__(self, page: Page):
        self.page = page

    def enter(self, text: str):
        if text is not None:
            self.page.fill("input#email", text)

    def is_displayed(self) -> bool:
        return self.page.is_visible("input#email")

    def get_error_message(self) -> str:
        error_selector = ".error-message, .error-message-show, .alert-general-error, .validation-email-error"
        if self.page.is_visible(error_selector):
            return self.page.inner_text(error_selector)
        return None

    def is_valid(self) -> bool:
        error_selector = ".error-message, .error-message-show, .alert-general-error, .validation-email-error"
        return not self.page.is_visible(error_selector)

    def clear(self):
        self.page.click("input#email")
        self.page.fill("input#email", "")

    @allure.step("Check, if Email field is empty")
    def is_email_field_empty(self) -> bool:
        return "ng-pristine" in self.page.locator("input#email").get_attribute("class")
