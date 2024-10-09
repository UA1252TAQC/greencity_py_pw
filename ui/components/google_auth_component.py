from playwright.sync_api import Page


class GoogleAuthComponent():
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("#identifierId")
        self.email_next_button = page.locator("#identifierNext div button")
        self.password_input = page.locator("#password div div div input")
        self.password_next_button = page.locator("#passwordNext div button")

    def enter_email(self, email: str):
        self.email_input.fill(email)
        return self

    def click_email_submit_button(self):
        self.email_next_button.click()
        return self

    def enter_password(self, password: str):
        self.password_input.fill(password)
        return self

    def click_password_submit_button(self):
        self.password_next_button.click()

    def is_email_input_displayed(self) -> bool:
        return self.email_input.is_visible()
