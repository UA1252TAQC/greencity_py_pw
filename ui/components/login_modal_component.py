import logging

import allure
from playwright.sync_api import Page
from ui.components.fields.email_field import EmailField
from ui.components.fields.password_field import PasswordField
from ui.components.component_factory import create_forgot_password_modal_component
from ui.components.google_auth_component import GoogleAuthComponent
from ui.pages.green_city.profile_page import ProfilePage

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


class LoginModalComponent:
    def __init__(self, page: Page):
        """
        Initializes the LoginModalComponent with necessary page elements.

        :param page: The Playwright page instance.
        """
        self.page = page
        self.app_sign_in = page.locator('app-sign-in')
        self.modal_component_element = page.locator("app-auth-modal .main")
        self.email = EmailField(page)
        self.password = PasswordField(page)
        self.sign_in_button = page.locator('button[type="submit"]')
        self.forgot_password_link = page.locator("//a[@class='forgot-password']")
        self.close_button = page.locator("img.cross-btn[alt='close button']")
        self.main_picture = page.locator("//img[@class='main-picture']")
        self.form_error_message = page.locator(".alert-general-error")
        self.sign_in_with_google = page.get_by_role("button", name="Google sign-in Sign in with")

    def login(self, email: str, password: str):
        """
        Logs in by entering the email and password, and clicking the sign-in button.

        :param email: Email address to be entered.
        :param password: Password to be entered.
        :return: The current instance of LoginModalComponent for chaining.
        """
        logger.info(f"Logging in with email: {email}")
        self.email.enter(email)
        self.password.enter(password)
        self.click_sign_in_button()
        logger.info("Clicked sign-in button")
        return self

    def enter_email(self, email: str):
        """
        Enters the email into the email field.

        :param email: Email address to be entered.
        :return: The current instance of LoginModalComponent for chaining.
        """
        logger.info(f"Entering email: {email}")
        self.email.enter(email)
        return self

    def enter_password(self, password: str):
        """
        Enters the password into the password field.

        :param password: Password to be entered.
        :return: The current instance of LoginModalComponent for chaining.
        """
        logger.info("Entering password (hidden for security reasons)")
        self.password.enter(password)
        return self

    def click_sign_in_button(self):
        """
        Waits for the sign-in button to appear and clicks it.

        :return: The current instance of LoginModalComponent for chaining.
        """
        logger.info("Clicking the sign-in button")
        self.page.wait_for_selector("button[type='submit']")
        self.sign_in_button.click()
        return self

    def click_sign_in_button_and_successful_login(self):
        """
        Clicks the 'Sign In' button and waits for a successful login.

        :return: ProfilePage object representing the user's profile page after a successful login.
        """
        self.click_sign_in_button()
        self.sign_in_button.wait_for(state='hidden')
        return ProfilePage(self.page)

    def click_forgot_password_link(self):
        """
        Clicks on the 'Forgot Password' link and returns the ForgotPasswordComponent.

        This method waits for the 'Forgot Password' link to be visible before clicking it.

        :return: ForgotPasswordComponent for further interactions with the 'Forgot Password' page or form.
        """
        self.forgot_password_link.wait_for(state='visible')
        self.forgot_password_link.click()
        return create_forgot_password_modal_component(self.page)

    def click_outside_form(self):
        """
        Clicks outside the form, for example, on the image.

        :return: The current instance of LoginModalComponent for chaining.
        """
        self.main_picture.click()
        return self

    def close(self):
        """
        Closes the current form by clicking the close button and waits for a short timeout.

        This method simulates a user closing the form and includes a 1-second timeout
        to ensure that any UI animations or transitions complete after the close button is clicked.
        """
        self.close_button.click()
        self.page.wait_for_timeout(1000)

    def get_login_error_text(self):
        """
        Get the login error message text if the error message element is present.

        Returns:
        - str: The text of the error message if found, otherwise a message indicating that the element was not found.
        """
        if self.form_error_message.is_visible():
            self.form_error_message.wait_for(state="visible")
            return self.form_error_message.text_content()
        else:
            return f"Element not found: {self.form_error_message}"

    @allure.step("Check if Sign-in button is active")
    def is_signin_btn_active(self) -> bool:
        return self.sign_in_button.is_enabled()

    @allure.step("Check if Sign-In Button is highlighted in {expected_color}")
    def is_highlighted_signin_btn_in_color(self, expected_color):
        background_color = self.sign_in_button.evaluate("element => getComputedStyle(element).backgroundColor")
        return background_color == expected_color

    @allure.step("Click \"Sign-in\" with Google")
    def click_signin_with_google_btn(self):
        with self.page.context.expect_page() as new_page_info:
            self.sign_in_with_google.click()
        active_page = new_page_info.value
        active_page.wait_for_load_state()
        active_page.bring_to_front()
        return GoogleAuthComponent(active_page)

    def is_login_form_displayed(self):
        return self.app_sign_in.is_visible()
