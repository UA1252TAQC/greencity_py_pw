import allure
import pytest
from playwright.sync_api import sync_playwright
from modules.dataprovider import DataProvider
from modules.localization_utils import LocalizationUtils
from ui.pages.green_city.green_city_home_page import GreenCityHomePage
from modules.constants import Data


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def initialize_page(playwright_instance, request):
    browser = playwright_instance.chromium.launch(
        headless=False
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    language = request.config.getoption("--language", default="Ua")
    localization_utils = LocalizationUtils(language=language)
    page.goto(f"{Data.UI_BASE_URL}greenCity")

    home_page = GreenCityHomePage(page)
    home_page.header_component.set_language(language)
    yield home_page, localization_utils
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def setup_function(initialize_page):
    home_page, localization_utils = initialize_page
    form = home_page.header_component.open_registration_form()
    yield form, localization_utils
    form.close()


@allure.title("Verify registration email field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form email field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, is_should_submit_form, error_message, email, username, password, repeat_password",
    DataProvider.get_ui_test_data("testEmailValidation"),
)
def test_email_validation(
    is_expected_valid,
    expected_error_message,
    is_should_submit_form,
    error_message,
    email,
    username,
    password,
    repeat_password,
    setup_function
):
    form, localization_utils = setup_function
    form.fill_form(email, username, password, repeat_password).submit_if(is_should_submit_form)

    is_actual_valid = form.email.is_valid()
    actual_error_message = form.email.get_error_message()

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message),"Error message mismatch"


@allure.title("Verify registration username field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form username field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, username",
    DataProvider.get_ui_test_data("testUsernameValidation"),
)
def test_username_validation(
    is_expected_valid, expected_error_message, error_message, username, setup_function
):
    form, localization_utils = setup_function
    form.enter_username(username).click_title()

    is_actual_valid = form.username.is_valid()
    actual_error_message = form.username.get_error_message()

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message ), "Error message mismatch"


@allure.title("Verify registration password field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form password field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, password",
    DataProvider.get_ui_test_data("testPasswordValidation"),
)
def test_password_validation(is_expected_valid, expected_error_message, error_message, password, setup_function):
    form, localization_utils = setup_function
    form.enter_password(password).click_title()

    is_actual_valid = form.password.is_valid()
    actual_error_message = form.password.get_error_message()

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"


@allure.title("Verify registration repeat password field validation")
@allure.description("""
    This test checks the validation of the registration form fields.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Green City")
@allure.feature("Registration form")
@allure.story("Registration form repeat password field validation")
@allure.tag("Green City")
@allure.issue("12")
@pytest.mark.parametrize(
    "is_expected_valid, expected_error_message, error_message, password, repeat_password",
    DataProvider.get_ui_test_data("testRepeatPasswordValidation"),
)
def test_repeat_password_validation(
    is_expected_valid,
    expected_error_message,
    error_message,
    password,
    repeat_password,
    setup_function
):
    form, localization_utils = setup_function
    form.enter_password(password)
    form.enter_repeat_password(repeat_password).click_title()

    is_actual_valid = form.repeat_password.is_valid()
    actual_error_message = form.repeat_password.get_error_message()

    assert is_actual_valid == is_expected_valid, error_message
    assert actual_error_message == localization_utils.get_form_message(expected_error_message), "Error message mismatch"
