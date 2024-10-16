from tests.ui_tests.test_data.data_provider import data_provider
from ui.pages.green_city.create_news_page import CreateNewsPage
from modules.constants import Data
import pytest
import allure

from ui.pages.green_city.news_page import NewsPage

@allure.description("Verify that news with source link can be created")
@allure.feature("CreateNews")
@allure.issue("93")
@pytest.mark.parametrize("title, content, tags", [data_provider("news_data_valid")])
def test_create_news_with_link(setup_function, title, content, tags):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    news_page = NewsPage(page)

    ((create_news_page
     .fill_the_news_form(title,  tags, content, 'en'))
     .enter_source_link('http://localhost:4205/#/news')
     .click_publish_button())
    page.wait_for_url(f"{Data.UI_BASE_URL}/#/news")

    assert   news_page.is_news_displayed_with_title(title) == True





