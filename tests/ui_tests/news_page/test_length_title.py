import pytest
import allure

from tests.ui_tests.test_data.test_data import test_data
from ui.pages.green_city.create_news_page import CreateNewsPage
from ui.pages.green_city.news_page import NewsPage


@allure.description("Verify that news will be created when the user puts 170 characters in the ‘Title’ field")
@allure.feature("CreateNews")
@allure.issue("115")
@pytest.mark.parametrize("title, content, tags", [
    (test_data['title_length']['title'], test_data['news_publish']['content'], test_data['news_publish']['tags'])
])
def test_check_length_title(setup_function, title, content, tags):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    news_page = NewsPage(page)

    (create_news_page.fill_the_news_form(title, tags, content, language='en').click_publish_button())
    assert news_page.is_news_displayed_with_title(title)
