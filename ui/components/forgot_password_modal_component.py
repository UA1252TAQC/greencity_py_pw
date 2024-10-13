from playwright.sync_api import Page

from ui.components.fields.email_field import EmailField

class ForgotPasswordModalComponent:
    def __init__(self, page: Page):
        self.page = page
        self.email = EmailField(page)
        self.sign_in_button = page.locator(".sign-in-form button[type='submit']")
        self.back_to_sign_in_link = page.locator("div.mentioned-password a.green-link")

    def is_back_to_sign_in_link_displayed(self) -> bool:
        return self.back_to_sign_in_link.is_visible()

    def click_back_to_sign_in_link(self):
        from ui.components.login_modal_component import LoginModalComponent
        self.back_to_sign_in_link.click()
        self.back_to_sign_in_link.wait_for(state="hidden")
        return LoginModalComponent(self.page)
