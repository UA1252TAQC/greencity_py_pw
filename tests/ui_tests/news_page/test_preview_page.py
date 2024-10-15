import pytest
import allure

from tests.ui_tests.test_data.test_data import test_data
from ui.pages.green_city.create_news_page import CreateNewsPage
from ui.pages.green_city.news_preview_page import NewsPreviewPage


@allure.description("Verify that the user can see the 'Preview' page after clicking the 'Preview' button")
@allure.feature("CreateNews")
@allure.issue("79")
@pytest.mark.parametrize("title, content, tags", [
    (test_data['news_publish']['title'], test_data['news_publish']['content'], test_data['news_publish']['tags'])
])
def test_preview_page_is_appear(setup_function, title, content, tags):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    news_preview_page = NewsPreviewPage(page)

    create_news_page.fill_the_news_form(title, tags, content, language='en')
    assert create_news_page.news_preview_button_is_enabled()

    create_news_page.click_preview_button()
    assert news_preview_page.is_preview_page_displayed()
