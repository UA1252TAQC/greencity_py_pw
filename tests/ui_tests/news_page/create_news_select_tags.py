import allure
import pytest

from tests.ui_tests.test_data.data_provider import data_provider
from ui.pages.green_city.create_news_page import CreateNewsPage
from ui.style_constants.colors import Colors


@allure.description("Verify that news tags can be selected or deselected, and the button's color changes accordingly.")
@allure.feature("CreateNews")
@allure.issue("93")
@pytest.mark.parametrize("list1, list2", [data_provider("tags_lists")])
def test_select_unselect_tag(setup_function, list1, list2):
    page = setup_function

    create_news_page = CreateNewsPage(page)
    create_news_page.select_tags(list1, 'en')

    for tag in list1:
        background_color = create_news_page.get_tag_button_background_color(tag)
        assert background_color == Colors.PRIMARY_GREEN

    create_news_page.unselect_tags(list1, 'en')

    for tag in list1:
        background_color = create_news_page.get_tag_button_background_color(tag)
        assert background_color == Colors.PRIMARY_WHITE

    create_news_page.select_tags(list2, 'en')

    for tag in list2:
        background_color = create_news_page.get_tag_button_background_color(tag)
        assert background_color == Colors.PRIMARY_GREEN

    create_news_page.unselect_tags(list2, 'en')

    for tag in list2:
        background_color = create_news_page.get_tag_button_background_color(tag)
        assert background_color == Colors.PRIMARY_WHITE
