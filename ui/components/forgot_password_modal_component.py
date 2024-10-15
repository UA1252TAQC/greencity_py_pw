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
        Initializes the ForgotPasswordComponent with necessary page elements.

        :param page: The Playwright page instance.
        """
        self.page = page
        self.submit_button = page.locator("//div[@class='restore-password-container']//button[@type='submit']")
        self.back_to_signin_button = page.locator("//div[@class='mentioned-password']//a[@class='green-link']")
        self.email = EmailField(page)
        self.forgot_password_locator = page.locator("//div[@class='restore-password-container']")
        self.back_to_signin_link = page.locator("//div[@class='mentioned-password']//a[@class='green-link']")

    def enter_email(self, email: str):
        """
        Enter the email into the email field.

        :param email: Email to be entered.
        :return: Returns the current instance of ForgotPasswordComponent for chaining.
        """
        logger.info(f"Entering email: {email}")
        self.email.enter(email)
        return self

    def click_submit_button(self):
        """
        Clicks the submit button after entering the email.

        :return: Returns the UbsHomePage after successfully submitting the forgot password form.
        """
        logger.info("Clicking the submit button")
        self.page.wait_for_selector("button[type='submit']")
        self.submit_button.click()
        return UbsHomePage(self.page)

    def is_forgot_password_form_displayed(self):
        """
        Checks if the forgot password form is visible on the page.

        :return: Boolean indicating whether the forgot password form is displayed.
        """
        logger.info("Checking if the forgot password form is displayed")
        return self.forgot_password_form.is_visible()

    def click_back_to_sign_in_link(self):
        """
        Clicks the 'Back to Sign In' link and waits for the link to be hidden.

        :return: None
        """
        logger.info("Clicking the 'Back to Sign In' link")
        self.back_to_signin_link.click()
        self.back_to_signin_link.wait_for(state='hidden')
        return None

    def get_error_message(self):
        """
        Retrieves the error message associated with the email field.

        :return: The error message text if present, otherwise an empty string.
        """
        logger.info("Getting error message from the email field")
        return self.email.get_error_message()
