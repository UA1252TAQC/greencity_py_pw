from playwright.sync_api import Page

from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField
from ui.components.fields.repeat_password_field import RepeatPasswordField
from ui.components.fields.username_field import UsernameField
from ui.components.google_auth_component import GoogleAuthComponent


class RegistrationModalComponent:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title-text")
        self.register_button = page.locator("button[type='submit']")
        self.google_button = page.locator("button.google-sign-in")
        self.sign_in_link = page.locator("a.green-link[aria-label='sign in modal window']")
        self.close_button = page.locator("img.cross-btn[alt='close button']")
        self.email = EmailField(page)
        self.username = UsernameField(page)
        self.password = PasswordField(page)
        self.repeat_password = RepeatPasswordField(page)

    def enter_email(self, text: str):
        self.email.enter(text)
        return self

    def enter_username(self, text: str):
        self.username.enter(text)
        return self

    def enter_password(self, text: str):
        self.password.enter(text)
        return self

    def enter_repeat_password(self, text: str):
        self.repeat_password.enter(text)
        return self

    def open_auth_google_form(self):
        self.google_button.click()
        self.page.wait_for_timeout(15000)
        self.page.context.pages[-1].bring_to_front()
        return GoogleAuthComponent(self.page.context.pages[-1])

    def fill_form(self, email: str, username: str, password: str, repeat_password: str):
        return (self.enter_email(email)
                .enter_username(username)
                .enter_password(password)
                .enter_repeat_password(repeat_password)
                .click_title())

    def click_title(self):
        self.title.click()
        return self

    def is_registration_button_displayed(self) -> bool:
        return self.register_button.is_visible()

    def is_google_button_displayed(self) -> bool:
        return self.google_button.is_visible()

    def submit(self):
        if self.register_button.is_visible() and self.register_button.is_enabled():
            self.register_button.click()
        else:
            raise Exception("Registration button is not enabled")

    def is_registration_button_enabled(self) -> bool:
        return self.register_button.is_enabled()

    def submit_if(self, should_submit_form: bool):
        if should_submit_form:
            self.submit()

    def is_sign_in_link_displayed(self) -> bool:
        return self.sign_in_link.is_visible()

    def close(self):
        self.close_button.click()
        self.page.wait_for_timeout(1000)

    def clear_password_field_if(self, should_clear_password: bool):
        if should_clear_password:
            self.password.clear()
        return self
