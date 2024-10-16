from tests.ui_tests.test_data.data_provider import data_provider
from ui.pages.green_city.create_news_page import CreateNewsPage
from modules.constants import Data
import pytest
import allure
import os

from ui.pages.green_city.news_page import NewsPage


@allure.description("Verify that news with added image(png) can be created")
@allure.feature("CreateNews")
@allure.issue("91")
@pytest.mark.parametrize("title, content, tags", [data_provider("news_data_valid")])
def test_create_news_with_jpeg_img(setup_function, title, content, tags):
    page = setup_function

    def handle_response(response):
        if response.request.method == "POST" and "eco-news" in response.url:
            assert response.ok

    page.on("response", handle_response)

    create_news_page = CreateNewsPage(page)
    news_page = NewsPage(page)

    ((create_news_page
     .fill_the_news_form(title,  tags, content, 'en'))
     .add_image(os.path.abspath("../resources/fruit-1218166_1280.png"))
     .click_publish_button())
    page.wait_for_url(f"{Data.UI_BASE_URL}/#/news")

    assert news_page.is_news_displayed_with_title(title) is True
