from playwright.sync_api import Page


def create_green_city_header_component(page: Page):
    from ui.components.green_city_header_component import GreenCityHeaderComponent
    return GreenCityHeaderComponent(page)


def create_login_modal_component(page: Page):
    from ui.components.login_modal_component import LoginModalComponent
    return LoginModalComponent(page)


def create_forgot_password_modal_component(page: Page):
    from ui.components.forgot_password_modal_component import ForgotPasswordModalComponent
    return ForgotPasswordModalComponent(page)
