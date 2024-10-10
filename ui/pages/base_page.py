import time
from playwright.sync_api import Page, TimeoutError


class BasePage:
    TIME_TO_WAIT = 60000
    RETRY_INTERVAL = 100

    def __init__(self, page: Page):
        self.page = page

    def get_pop_up_message(self):
        max_retries = int(self.TIME_TO_WAIT / (self.RETRY_INTERVAL))
        for _ in range(max_retries):
            try:
                self.page.wait_for_selector("//div[@matsnackbarlabel]", timeout=self.RETRY_INTERVAL)
                elements = self.page.locator("//div[@matsnackbarlabel]").all()
                if elements is not None:
                    return elements[0].inner_text()
            except TimeoutError:
                time.sleep(self.RETRY_INTERVAL)
        raise TimeoutError(f"Timeout of {self.TIME_TO_WAIT}ms exceeded while waiting for pop-up message")

    def open_url_in_new_tab(self, url: str):
        self.page.evaluate(f"window.open('{url}', '_blank');")
        self.switch_to_active_tab()

    def switch_to_active_tab(self):
        tabs = self.page.context.pages
        self.page = tabs[-1]

    # def switch_to_active_tab(self):
    #     self.sleep(1)
    #     tabs = self.page.context.pages
    #     self.page = tabs[-1]

    # def get_local_storage_item(self, key: str):
    #     return self.page.evaluate(f"window.localStorage.getItem('{key}');")

    # def get_auth_token(self):
