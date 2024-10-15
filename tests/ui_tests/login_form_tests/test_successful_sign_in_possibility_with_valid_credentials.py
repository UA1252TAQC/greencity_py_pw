import pytest

from modules.constants import Data
from playwright.sync_api import Page, expect
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.mark.ui_login
def test_successful_sign_in_possibility(setup_function, check):
    page = setup_function
    page.goto(Data.UI_GREEN_CITY_HOME_PAGE_URL)
    profile_page = (
        GreenCityHomePage(page)
        .header_component.open_login_form()
        .enter_email(Data.USER_EMAIL)
        .enter_password(Data.USER_PASSWORD)
        .click_sign_in_button_and_successful_login()
    )

    # assert profile_page.page.url == f"{Data.UI_GREEN_CITY_PROFILE_PAGE_URL}/{Data.USER_ID}", "User profile url doesn't match"
    expect(profile_page.page).to_have_url(f"{Data.UI_GREEN_CITY_PROFILE_PAGE_URL}/{Data.USER_ID}")
    # expect(profile_page.header_component.username).to_contain_text(Data.USER_NAME)
    # expect(page).to_have_url(f"{Data.UI_GREEN_CITY_PROFILE_PAGE_URL}/{Data.USER_ID}100")
    # expect(page).to_have_url(f"{Data.UI_GREEN_CITY_PROFILE_PAGE_URL}/{Data.USER_ID}200")

    #     assert profile_page.header_component.get_username() == Data.USER_NAME, "User name don't match"
    #     assert profile_page.page.url == f"{Data.UI_BASE_URL}/#/profiles/{Data.USER_ID}", "User profile url doesn't match"
