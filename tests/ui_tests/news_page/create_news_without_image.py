from modules.fake_data_generator import generate_news_data
from ui.pages.green_city.create_news_page import CreateNewsPage
from modules.constants import Data
import pytest
import allure

from ui.pages.green_city.news_page import NewsPage


@allure.description("Verify that news without image can be created")
@allure.feature("CreateNews")
@allure.issue("75")
@pytest.mark.parametrize("title, content, tags", [generate_news_data()])
def test_create_news_without_image(setup_function, title, content, tags):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    news_page = NewsPage(page)

    ((create_news_page
     .fill_the_news_form(title,  tags, content, 'en'))
     .click_publish_button())
    page.wait_for_url(f"{Data.UI_BASE_URL}/#/news")

    assert news_page.is_news_displayed_with_title(title) is True
