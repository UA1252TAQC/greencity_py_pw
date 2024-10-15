from playwright.sync_api import Page

from ui.pages.green_city.green_city_base_page import GreenCityBasePage
import allure


class NewsPreviewPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_to_editing_button = page.locator(PreviewNewsPageLocators.PREVIEW_PAGE_TITLE)
        self.preview_page_title = page.locator(PreviewNewsPageLocators.PREVIEW_PAGE_TITLE)

    @allure.step("Click 'Back to Editing' button")
    def click_back_to_editing(self):
        self.back_to_editing_button.click()
        return self

    @allure.step("Verify if preview page is displayed")
    def is_preview_page_displayed(self):
        return self.preview_page_title.is_visible()


class PreviewNewsPageLocators:
    PREVIEW_PAGE_TITLE = "div.news-title.word-wrap"
    BACK_TO_EDITING = "div.back-button a"
