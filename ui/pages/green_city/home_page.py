from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.wait_for_selector("//header[@role='banner']", timeout=20000)

    def set_language(self, language: str):
        self.page.click(f"//button[@data-language='{language}']")
        return self