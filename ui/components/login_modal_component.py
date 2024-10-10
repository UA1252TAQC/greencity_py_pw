from playwright.sync_api import Page

from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField
# from ui.pages.green_city.profile_page import ProfilePage


class LoginModalComponent:
    def __init__(self, page: Page):
        self.page = page
        self.email = EmailField(page)
        self.password = PasswordField(page)
        self.signInButton = page.locator("button[@type='submit']")

    def fill_form(self, email: str, password: str):
        self.email.enter(email)
        self.password.enter(password)
        return self

    def click_sign_in_button_successfull_login(self):
        self.signInButton.click()
        # return ProfilePage(self.page)
