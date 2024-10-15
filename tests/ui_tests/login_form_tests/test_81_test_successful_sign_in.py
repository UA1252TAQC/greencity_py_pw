import allure
import logging as log

from modules.constants import Data


@allure.description("Verify the Sign-In possibility with valid credentials")
@allure.feature("Login")
@allure.issue("81")
def test_successful_sign_in(initialize_page, tc_logger):
    test_name = "Verify the Sign-In possibility with valid credentials."
    tc_logger.log_test_name(test_name)
    log.info(f"Test '{test_name}' started")

    expected_username = Data.USER_NAME
    expected_url = f"{Data.UI_BASE_URL}/#/profile/{Data.USER_ID}"

    try:
        profile_page = (
            initialize_page
            .header_component.open_login_form()
            .enter_email(Data.USER_EMAIL)
            .enter_password(Data.USER_PASSWORD)
            .click_sign_in_button_and_successful_login()
        )

        actual_url = profile_page.page.url
        assert actual_url == expected_url, (
            f"Expected URL: {expected_url}, but got: {actual_url}"
        )
        log.info(f"Page URL verification passed: {actual_url}")

        actual_username = profile_page.header_component.get_username()
        assert actual_username == expected_username, (
            f"Expected username: '{expected_username}', but got: '{actual_username}'"
        )
        log.info(f"Username verification passed: {actual_username}")

        log.info(f"Test '{test_name}' completed successfully.")

    except AssertionError as ae:
        log.error(f"Assertion failed in '{test_name}': {str(ae)}")
        raise

    except Exception as e:
        log.error(f"An unexpected error occurred during '{test_name}': {str(e)}")
        raise

    finally:
        log.info(f"Test '{test_name}' finished.")
