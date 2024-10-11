from playwright.sync_api import Page

from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField


class LoginModalComponent:
    def __init__(self, page: Page):
        """
        Initialize the LoginModalComponent with necessary page elements.
        """
        self.page = page
        self.email = EmailField(page)
        self.password = PasswordField(page)
        self.sign_in_button = page.locator(".sign-in-form button[type='submit']")

    def login(self, email: str, password: str):
        """
        Enter email, password, and click the sign-in button.
        :param email: Email address to be entered.
        :param password: Password to be entered.
        """
        self.email.enter(email)
        self.password.enter(password)
        self.click_sign_in_button()
        return self

    def click_sign_in_button(self):
        """
        Wait for the sign-in button to appear and click it.
        """
        self.page.wait_for_selector("button[type='submit']")
        self.sign_in_button.click()
        return self

    def click_sign_in_button_and_wait_for_success(self):
        """
        Click the sign-in button and wait until it disappears (indicating successful login).
        """
        self.click_sign_in_button()
        self.sign_in_button.wait_for(state='hidden')
        return self
