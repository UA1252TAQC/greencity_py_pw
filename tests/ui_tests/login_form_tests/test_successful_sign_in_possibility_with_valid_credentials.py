import pytest

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


# @pytest.mark.ui_login
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

    # with check:
    assert profile_page.page.url == f"{Data.UI_GREEN_CITY_PROFILE_PAGE_URL}/{Data.USER_ID}", "User profile url doesn't match"
    # with check:
    #     assert profile_page.header_component.get_username() == Data.USER_NAME, "User name don't match"
    # with check:
    #     assert profile_page.page.url == f"{Data.UI_BASE_URL}/#/profiles/{Data.USER_ID}", "User profile url doesn't match"
