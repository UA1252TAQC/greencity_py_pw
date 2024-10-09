from playwright.sync_api import Page


class BasePage():
    TIME_TO_WAIT = 15000

    def __init__(self, page: Page):
        self.page = page
        self.header_root_element = self.find_with_wait_element("//header[@role='banner']", self.TIME_TO_WAIT)

    def get_pop_up_message(self):
        return self.find_with_wait_element("//div[@matsnackbarlabel]", self.TIME_TO_WAIT).inner_text()

    def open_url(self, url: str):
        self.page.goto(url)

    def open_url_in_new_tab(self, url: str):
        self.page.evaluate(f"window.open('{url}', '_blank');")
        self.switch_to_active_tab()

    def switch_to_active_tab(self):
        self.sleep(1)
        tabs = self.page.context.pages
        self.page = tabs[-1]

    def get_local_storage_item(self, key: str):
        return self.page.evaluate(f"window.localStorage.getItem('{key}');")

    def get_auth_token(self):
        return self.get_local_storage_item("accessToken")

    def get_current_url(self):
        return self.page.url
