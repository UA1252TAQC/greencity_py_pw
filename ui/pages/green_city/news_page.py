from playwright.sync_api import Page

from ui.enum.news_tags import NewsTags
from ui.pages.green_city.green_city_base_page import GreenCityBasePage
import allure


class NewsPage(GreenCityBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_news_button = page.locator(NewsPageLocators.CREATE_NEWS_BUTTON)
        self.author_name = self.page.locator(NewsPageLocators.AUTH_NAME)

    @allure.step("Click 'Create News' button")
    def click_create_news(self, page):
        self.create_news_button.click()
        from ui.pages.green_city.create_news_page import CreateNewsPage
        return CreateNewsPage(self.page)

    @allure.step("Verify if news is displayed by title, content and tags")
    def is_news_displayed(self, title: str, content: str, tags: list[NewsTags]) -> bool:
        news_items = self.page.locator(NewsPageLocators.NEWS_ITEM_BOX).all()

        for item in news_items:
            is_title_present = item.locator("xpath=.//h3[contains(text(), '" + title + "')]").count() > 0
            is_content_present = item.locator("xpath=.//p[contains(text(), '" + content + "')]").count() > 0

            is_tags_present = True
            for tag in tags:
                added_tag_ua = item.locator(f".ul-eco-buttons:has-text('{tag.get_text('ua')}')").count() > 0
                added_tag_en = item.locator(f".ul-eco-buttons:has-text('{tag.get_text('en')}')").count() > 0
                is_tags_present = is_tags_present and (added_tag_ua or added_tag_en)

            result = is_title_present and is_content_present and is_tags_present
            if result:
                return result

        return False

    @allure.step("Verify if news is displayed by title")
    def is_news_displayed_with_title(self,  title: str):
        news_items = self.page.locator("//div[@class='list-gallery']").all()

        for item in news_items:
            is_title_present = item.locator("xpath=.//h3[contains(text(), '" + title + "')]").count() > 0
            if is_title_present:
                return True

        return False

    @allure.step("Click on news item by title")
    def click_on_news_with_title(self, title):
        news_items = self.page.locator("//div[@class='list-gallery']").all()
        for item in news_items:
            title_element = item.locator("xpath=.//h3[contains(text(), '" + title + "')]")
            if title_element.count() > 0:
                title_element.click()
                return

        raise TimeoutError(f"News with title '{title}' was not found.")

    @allure.step("Get author Name")
    def get_author_name(self) -> str:
        return self.author_name.text_content().strip()


class NewsPageLocators:
    CREATE_NEWS_BUTTON = "//a[contains(@class,'create')]//div[@id='create-button']"
    NEWS_ITEM_BOX = "app-news-list-gallery-view"
    AUTH_NAME = "//div[@class='news-info-author']"
