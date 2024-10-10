from playwright.sync_api import Page


class BasePage:
    TIME_TO_WAIT = 60000

    def __init__(self, page: Page):
        self.page = page
        page.wait_for_timeout(2000)

    def get_pop_up_message(self):
        return self.page.wait_for_selector("//div[@matsnackbarlabel]", timeout=self.TIME_TO_WAIT).inner_text()

    def open_url_in_new_tab(self, url: str):
        self.page.evaluate(f"window.open('{url}', '_blank');")
        self.switch_to_active_tab()

    def switch_to_active_tab(self):
        self.page.wait_for_timeout(10000)
        tabs = self.page.context.pages
        if (len(tabs) > 1):
            tabs[-1].bring_to_front()
            self.page = tabs[-1]
        else:
            tabs[0].bring_to_front()
            self.page = tabs[0]

    # def switch_to_active_tab(self):
    #     self.sleep(1)
    #     tabs = self.page.context.pages
    #     self.page = tabs[-1]

    def get_local_storage_item(self, key: str):
        return self.page.evaluate(f"window.localStorage.getItem('{key}');")

    def get_auth_token(self):
        return self.get_local_storage_item("accessToken")
