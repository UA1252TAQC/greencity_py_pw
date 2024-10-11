from playwright.sync_api import Page

from ui.pages.green_city.create_news_page import CreateNewsPage
from ui.pages.green_city.green_city_base_page import GreenCityBasePage


class NewsPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_news_button = page.locator(NewsPageLocators.CREATE_NEWS_BUTTON)

    def click_create_news(self, page):
        self.create_news_button.click()
        return CreateNewsPage(self.page)


class NewsPageLocators:
    CREATE_NEWS_BUTTON = "a[contains(@class,'create')]//div[@id='create-button']"
    NEWS_ITEM_BOX = "app-news-list-gallery-view"
