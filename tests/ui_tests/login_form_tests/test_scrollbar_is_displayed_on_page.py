import pytest

from modules.constants import Data
from ui.pages.green_city.green_city_home_page import GreenCityHomePage


@pytest.mark.ui_login
@pytest.mark.parametrize("width", [320])
def test_successful_sign_in_possibility(setup_function, check, width):
    page = setup_function
    page.goto(Data.UI_GREEN_CITY_HOME_PAGE_URL)
    login_form = (GreenCityHomePage(page)
                  .header_component.set_language('en')
                  .open_login_form())

    assert login_form.is_forgot_password_link_displayed() is True

    page.set_viewport_size({"width": width, "height": page.viewport_size['height']})

    assert page.viewport_size['width'] == width

    # scroll_height = login_form.sign_in_button('element => element.scrollHeight')
    # client_height = login_form.sign_in_button('element => element.clientHeight')
    page.pause()
    zoom = 150
    page.evaluate(f"document.body.style.zoom = '{zoom}%'")

    zoom_value = page.evaluate("window.getComputedStyle(document.body).zoom")

    # assert scroll_height == 100
    # assert client_height == 100
    assert zoom_value == 1000


