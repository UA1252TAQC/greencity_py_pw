import allure
from playwright.sync_api import Page


class PasswordField:
    def __init__(self, page: Page):
        self.page = page

    def enter(self, text: str):
        if text is not None:
            self.page.fill("input#password", text)

    def is_displayed(self) -> bool:
        return self.page.is_visible("input#password")

    def get_error_message(self) -> str:
        error_selector = ".alert-general-error, #pass-err-msg div"
        if self.page.is_visible(error_selector):
            return self.page.inner_text(error_selector)
        return None

    def is_valid(self) -> bool:
        error_selector = ".alert-general-error, #pass-err-msg div"
        return not self.page.is_visible(error_selector)

    def clear(self):
        self.page.click("input#password")
        self.page.fill("input#password", "")

    @allure.step("Check, if Password field is empty")
    def is_password_field_empty(self) -> bool:
        return "ng-pristine" in self.page.get_attribute("input#password", "class")
