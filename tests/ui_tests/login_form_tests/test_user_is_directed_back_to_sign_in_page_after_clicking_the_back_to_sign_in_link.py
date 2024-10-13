import pytest

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


# @pytest.mark.ui_login
def test_successful_sign_in_possibility(setup_function, check):
    page = setup_function
    page.goto(Data.UI_GREEN_CITY_HOME_PAGE_URL)
    forgot_password_form = ((GreenCityHomePage(page)
                            .header_component.set_language('en')
                            .open_login_form())
                            .click_forgot_password_link())


    assert forgot_password_form.is_back_to_sign_in_link_displayed() == True

    login_form = (forgot_password_form
                  .click_back_to_sign_in_link())

    assert login_form.is_forgot_password_link_displayed() == True
