import pytest
import allure

from tests.ui_tests.test_data.test_data import test_data
from modules.constants import Data
from ui.pages.green_city.create_news_page import CreateNewsPage
from ui.pages.green_city.news_page import NewsPage


@allure.description("Verify that Author (registered User nickname) is Auto-filled")
@allure.feature("CreateNews")
@allure.issue("77")
@pytest.mark.parametrize("title, content, tags", [
    (test_data['author_field']['title'], test_data['news_publish']['content'], test_data['news_publish']['tags'])
])
def test_publish_news(setup_function, title, content, tags):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    news_page = NewsPage(page)

    create_news_page.fill_the_news_form(title, tags, content, language='en')
    create_news_page.click_publish_button().click_on_news_with_title(title)

    actual_author_name = news_page.get_author_name()

    expected_author_name = f"by {Data.USER_NAME}"
    assert actual_author_name == expected_author_name, \
        f"Expected author name: {expected_author_name}, but got: {actual_author_name}"
