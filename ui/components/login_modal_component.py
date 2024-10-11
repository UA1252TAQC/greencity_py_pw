from playwright.sync_api import Page

from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField
from ui.pages.green_city.profile_page import ProfilePage


class LoginModalComponent:
    def __init__(self, page: Page):
        self.page = page
        self.email = EmailField(page)
        self.password = PasswordField(page)
        self.sign_in_button = page.locator("button[type='submit']")

    def enter_email(self, email: str):
    def fill_form(self, email: str, password: str):
        self.email.enter(email)
        return self

    def enter_password(self, password: str):
        self.password.enter(password)
        return self

    def click_sign_in_button(self):
        self.sign_in_button.click()
        return self

    def click_sign_in_button_and_successful_login(self):
        self.click_sign_in_button()
        self.sign_in_button.wait_for(state='hidden')
        return ProfilePage(self.page)
