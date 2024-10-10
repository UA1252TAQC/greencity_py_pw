from playwright.sync_api import Page


class BaseComponent:
    def __init__(self, page: Page):
        self.page = page
        # self.root_element = root_element
        # self.page.locator(root_element)
