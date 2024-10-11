from playwright.sync_api import Page
from ui.components.regisration_modal_component import RegistrationModalComponent
from ui.components.login_modal_component import LoginModalComponent


class GreenCityHeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.logo = page.locator(".header_logo")
        self.news = page.locator(".header_navigation-menu li:nth-child(1) a")
        self.current_language = page.locator("ul[aria-label='language switcher']")
        self.list_language = page.locator("ul[aria-label='language switcher'] li[aria-label='english']")
        self.english = page.locator("li[aria-label='En']")
        self.ukrainian = page.locator("li[aria-label='Ua']")
        self.login = page.locator("a.header_sign-in-link")
        self.register = page.locator("li.header_sign-up-link span")
        self.login_root_element = page.locator("app-auth-modal")
        self.registration_root_element = page.locator("app-auth-modal")

    def open_registration_form(self):
        self.register.click()
        return RegistrationModalComponent(self.page)

    def open_login_form(self):
        self.login.click()
        return LoginModalComponent(self.page)

    def set_language(self, language: str):
        current_language = self.current_language.inner_text()
        if current_language.strip().lower() == language.lower():
            return
        self.list_language.click()
        if language.lower() == "en":
            self.english.click()
        elif language.lower() == "ua":
            self.ukrainian.click()

    def get_username(self) -> str:
        return self.page.locator("#header_user-wrp li.user-name").inner_text().strip()
