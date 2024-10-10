from playwright.sync_api import Page

from ui.components.regisration_modal_component import RegistrationModalComponent


class UbsHeaderComponent():
    def __init__(self, page: Page):
        self.page = page
        self.current_language = page.locator("ul[aria-label='language switcher']")
        self.list_language = page.locator(
            "ul.header_lang-switcher-wrp.header_navigation-menu-right-lang.ubs-lang-switcher")
        self.english = page.locator("li[aria-label='EN']")
        self.ukrainian = page.locator("li[aria-label='UA']")
        self.register = page.locator("li.header_sign-up-link.ng-star-inserted span")
        self.auth_root_element = page.locator("app-auth-modal")

    def open_registration_form(self):
        self.register.click()
        return RegistrationModalComponent(self.page)

    def set_language(self, language: str):
        c_language = self.current_language.inner_text()
        if c_language.strip().lower() == language.lower():
            return
        self.list_language.click()
        self.page.wait_for_timeout(1000)
        if language.lower() == "en":
            self.english.click()
        elif language.lower() == "ua":
            self.ukrainian.click()
