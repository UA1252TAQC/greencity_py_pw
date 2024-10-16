import allure
from playwright.sync_api import Page

from ui.components.login_modal_component import LoginModalComponent
from ui.components.regisration_modal_component import RegistrationModalComponent
from ui.pages.green_city.news_page import NewsPage


class GreenCityHeaderComponent:
    def __init__(self, page: Page):
        self.page = page
        self.logo = page.locator(".header_logo")
        self.news = page.locator('.header_navigation-menu a[href*="news"]')
        self.current_language = page.locator("ul[aria-label='language switcher']")
        self.list_language = page.locator("ul[aria-label='language switcher'] li[aria-label='english']")
        self.english = page.locator("li[aria-label='En']")
        self.ukrainian = page.locator("li[aria-label='Ua']")
        self.login = page.locator("a.header_sign-in-link")
        self.register = page.locator("li.header_sign-up-link span")
        self.login_root_element = page.locator("app-auth-modal")
        self.registration_root_element = page.locator("app-auth-modal")
        self.username_selector = "//*[@id='header_user-wrp']/li"

    @allure.step("Open registration form")
    def open_registration_form(self):
        self.register.click()
        return RegistrationModalComponent(self.page)

    @allure.step("Set language to {language}")
    def set_language(self, language: str):
        current_language = self.current_language.inner_text()
        if current_language.strip().lower() == language.lower():
            return self
        self.list_language.click()
        if language.lower() == "en":
            self.english.click()
            return self
        elif language.lower() == "ua":
            self.ukrainian.click()
            return self

    def get_username(self):
        return self.page.wait_for_selector(self.username_selector).inner_text().strip()

    def open_news_link(self):
        self.news.click()
        return NewsPage(self.page)

    def open_login_form(self):
        self.login.click()
        return LoginModalComponent(self.page)
