from playwright.sync_api import Page

from ui.components.fields import EmailField, UsernameField, PasswordField, RepeatPasswordField
from ui.components.google_auth_component import GoogleAuthComponent


class RegistrationModalComponent:
    def __init__(self, page: Page):
        self.page = page
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
        self.page.click(".google-sign-in")
        self.page.wait_for_timeout(1000)
        self.page.context.pages[-1].bring_to_front()
        return GoogleAuthComponent(self.page.context.pages[-1])

    def fill_form(self, email: str, username: str, password: str, repeat_password: str):
        return (self.enter_email(email)
                .enter_username(username)
                .enter_password(password)
                .enter_repeat_password(repeat_password)
                .click_title())

    def click_title(self):
        self.page.click(".title-text")
        return self

    def is_registration_button_displayed(self):
        return self.page.is_visible(".//button[@type='submit']")

    def is_google_button_displayed(self):
        return self.page.is_visible(".google-sign-in")

    def submit(self):
        self.page.click(".//button[@type='submit']")

    def is_registration_button_enabled(self):
        return self.page.is_enabled(".//button[@type='submit']")

    def submit_if(self, should_submit_form: bool):
        if should_submit_form:
            self.submit()

    def is_sign_in_link_displayed(self):
        return self.page.is_visible(".green-link")

    def close(self):
        self.page.click(".cross-btn[alt='close button']")
        self.page.wait_for_timeout(1000)

    def clear_password_field_if(self, should_clear_password: bool):
        if should_clear_password:
            self.password.clear()
        return self
