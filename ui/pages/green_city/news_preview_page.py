from playwright.sync_api import Page

from ui.pages.green_city.green_city_base_page import GreenCityBasePage


class NewsPreviewPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_to_editing_button = page.locator(PreviewNewsPageLocators.PREVIEW_PAGE_TITLE)
        self.preview_page_title = page.locator(PreviewNewsPageLocators.PREVIEW_PAGE_TITLE)

    def click_back_to_editing(self):
        self.back_to_editing_button.click()
        return self

    def is_preview_page_displayed(self):
        return self.preview_page_title.is_visible()


class PreviewNewsPageLocators:
    PREVIEW_PAGE_TITLE = ".//div[@class='news-title word-wrap']"
    BACK_TO_EDITING = "//div[@class = 'back-button']/a"
