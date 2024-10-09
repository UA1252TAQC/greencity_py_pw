from playwright.sync_api import Page


class GoogleAuthComponent:
    def __init__(self, page: Page):
        self.page = page

    def enter_email(self, email: str):
        self.page.fill("#identifierId", email)
        return self

    def click_email_submit_button(self):
        self.page.click("#identifierNext div button")
        self.page.wait_for_timeout(6000)
        return self

    def enter_password(self, password: str):
        self.page.fill("#password div div div input", password)
        return self

    def click_password_submit_button(self):
        self.page.click("#passwordNext div button")
        self.page.wait_for_timeout(1000)

    def is_email_input_displayed(self) -> bool:
        return self.page.is_visible("#identifierId")
