from playwright.sync_api import Page

def create_login_modal_component(page: Page):
    from ui.components.login_modal_component import LoginModalComponent
    return LoginModalComponent(page)

def create_forgot_password_modal_component(page: Page):
    from ui.components.forgot_password_modal_component import ForgotPasswordModalComponent
    return ForgotPasswordModalComponent(page)