import allure
import logging as log

import pytest


@allure.description("Verify that the scrollbar is displayed on the Sign In page")
@allure.feature("Login")
@allure.issue("98")
@allure.issue("99")
@allure.issue("100")
@allure.issue("101")
@allure.issue("102")
@pytest.mark.login
@pytest.mark.parametrize(
    "width, zoom_list",
    [
        (320, [100, 125, 150, 200]),
        (576, [100, 125, 150, 200]),
        (768, [100, 125, 150, 200]),
        (1024, [100, 125, 150, 200]),
        (1440, [100, 125, 150, 200])
    ]
)
def test_scrollbar_is_displayed_on_page(initialize_page, tc_logger, width, zoom_list):
    test_name = "Verify that the scrollbar is displayed on the Sign In page"
    tc_logger.log_test_name(test_name)
    log.info(f"Test '{test_name}' started")

    try:
        login_form = (initialize_page.header_component
                      .set_language('en')
                      .open_login_form())

        height = login_form.page.viewport_size['height']
        login_form.page.set_viewport_size({"width": width, "height": height})

        assert login_form.page.viewport_size[
                   'width'] == width, f"Expected width: {width}, but got {login_form.page.viewport_size['width']}"
        log.info(f"Viewport set to width: {width}px, height: {height}px")

        for zoom in zoom_list:
            login_form.page.evaluate(f"document.body.style.zoom = '{zoom}%'")
            log.info(f"Zoom level set to {zoom}%")

            expected_zoom_value = login_form.page.evaluate("window.getComputedStyle(document.body).zoom")
            log.info(f"Computed zoom value after setting: {expected_zoom_value}")

            scroll_width = login_form.modal_component_element.evaluate("el => el.scrollWidth")
            client_width = login_form.modal_component_element.evaluate("el => el.clientWidth")
            element_width = login_form.modal_component_element.evaluate("el => el.offsetWidth") * zoom / 100

            scrollbar_should_be_displayed_on_page = element_width > width
            scrollbar_is_displayed = scroll_width > client_width

            log.info(
                f"Zoom: {zoom}% | Scroll Width: {scroll_width}px | Client Width: {client_width}px |"
                f" Window width: {width} | Element Width (adjusted for zoom): {element_width}px")

            assert scrollbar_is_displayed == scrollbar_should_be_displayed_on_page

    except Exception as e:
        log.error(f"Test '{test_name}' failed due to error: {str(e)}")
        pytest.fail(f"Test '{test_name}' failed due to an unexpected error: {str(e)}")

    log.info(f"Test '{test_name}' completed")
