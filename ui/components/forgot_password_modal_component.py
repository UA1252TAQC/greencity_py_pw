import logging

from playwright.sync_api import Page
from ui.components.fields.email_field import EmailField
from ui.pages.ubs.ubs_home_page import UbsHomePage

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


class ForgotPasswordComponent:
    def __init__(self, page: Page):
        """
        Initialize the LoginModalComponent with necessary page elements.
        """
        self.page = page
        self.submit_button = page.locator("//div[@class='restore-password-container']//button[@type='submit']")
        self.back_to_signin_button = page.locator("//div[@class='mentioned-password']//a[@class='green-link']")
        self.email = EmailField(page)
        self.forgot_password_form = page.locator("//div[@class='restore-password-container']")
        self.back_to_signin_link = page.locator(".//div[@class='mentioned-password']//a[@class='green-link']")

    def enter_password(self, password: str):
        """
        Enter the password into the password field.
        :param password: Password to be entered.
        :return: Returns the current instance of LoginModalComponent for chaining.
        """
        self.logger.info("Entering password (hidden for security reasons)")
        self.password.enter(password)
        return self

    def click_sign_in_button(self):
        """
        Wait for the sign-in button to appear and click it.
        """
        logger.info("Clicking the sign-in button")
        self.page.wait_for_selector("button[type='submit']")
        self.sign_in_button.click()
        return UbsHomePage(self.page)

    def is_forgot_password_form_displayed(self):
        return self.forgot_password_form.is_visible()

    def click_back_to_sign_in_link(self):
        self.back_to_signin_link.click()
        self.back_to_signin_link.wait_for(state='hidden')
        return LoginModalComponent(self.page)

    def get_error_message(self):
        return self.email.get_error_message()
