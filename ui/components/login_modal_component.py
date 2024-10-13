import logging

from playwright.sync_api import Page
from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField
from ui.components.forgot_password_modal_component import ForgotPasswordModalComponent
from ui.pages.green_city.green_city_profile_page import GreenCityProfilePage

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


class LoginModalComponent:
    def __init__(self, page: Page):
        """
        Initialize the LoginModalComponent with necessary page elements.
        """
        self.page = page
        self.modal_component_element = page.locator("app-auth-modal div")
        self.email = EmailField(page)
        self.password = PasswordField(page)
        self.sign_in_button = page.locator(".sign-in-form button[type='submit']")
        self.forgot_password_link = page.locator("a.forgot-password")

    def login(self, email: str, password: str):
        """
        Enter email, password, and click the sign-in button.
        :param email: Email address to be entered.
        :param password: Password to be entered.
        """
        logger.info(f"Logging in with email: {email}")
        self.email.enter(email)
        self.password.enter(password)
        self.click_sign_in_button()
        logger.info("Clicked sign-in button")
        return self

    def enter_email(self, email: str):
        """
        Enter the email into the email field.
        :param email: Email address to be entered.
        :return: Returns the current instance of LoginModalComponent for chaining.
        """
        logger.info(f"Entering email: {email}")
        self.email.enter(email)
        return self

    def enter_password(self, password: str):
        """
        Enter the password into the password field.
        :param password: Password to be entered.
        :return: Returns the current instance of LoginModalComponent for chaining.
        """
        logger.info("Entering password (hidden for security reasons)")
        self.password.enter(password)
        return self

    def click_sign_in_button(self):
        """
        Wait for the sign-in button to appear and click it.
        """
        logger.info("Clicking the sign-in button")
        self.page.wait_for_selector("button[type='submit']")
        self.sign_in_button.click()
        return self

    def click_sign_in_button_and_successful_login(self):
        self.click_sign_in_button()
        self.sign_in_button.wait_for(state='hidden')
        return GreenCityProfilePage(self.page)

    def is_forgot_password_link_displayed(self) -> bool:
        return self.forgot_password_link.is_visible()

    def click_forgot_password_link(self):
        self.forgot_password_link.click()
        return ForgotPasswordModalComponent(self.page)
