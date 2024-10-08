import pytest
import allure
from api.base_api import BaseApi
from http import HTTPStatus
from modules.constants import Data
from modules.dataprovider import DataProvider


@allure.title("Get all eco news")
@allure.description("""
    This test checks the response of the request to get all eco news.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Eco News")
@allure.feature("Get all eco news")
@allure.story("Get all eco news")
@allure.tag("Eco News")
def test_get_eco_news_default():
    api = BaseApi(f"{Data.BASE_URL}eco-news")
    response = api.get_data()
    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert "page" in json_response
    for news in json_response["page"]:
        assert "id" in news
        assert "title" in news
        assert "content" in news
        assert "shortInfo" in news
        assert "author" in news
        assert "creationDate" in news
        assert "imagePath" in news
        assert "source" in news
        assert "tagsUa" in news
        assert "tagsEn" in news
        assert "likes" in news
        assert "countComments" in news
        assert "countOfEcoNews" in news


@allure.title("Get all eco news with tags")
@allure.description("""
    This test checks the response of the request to get all eco news with tags.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Eco News")
@allure.feature("Get all eco news")
@allure.story("Get all eco news with tags")
@allure.tag("Eco News")
@pytest.mark.parametrize(
    "expected_size, tags",
    DataProvider.get_data("test_get_all_eco_news_with_tags")
)
def test_get_all_eco_news_with_tags(expected_size, tags):
    api = BaseApi(f"{Data.BASE_URL}eco-news")
    actual_response = api.get_data(query_params={"tags": tags})
    assert actual_response.status_code == HTTPStatus.OK
    actual_json_response = actual_response.json()
    assert actual_json_response["totalElements"] == expected_size, (
        f"Expected {expected_size} news, but got {actual_json_response["totalElements"]}"
    )
    for news in actual_json_response["page"]:
        assert "tagsEn" in news, (
            f"Expected 'tags' key in news, but got {news}"
        )
        assert any(tag in news["tagsEn"] for tag in tags), (
            f"Expected tags {tags}, but got {news['tagsEn']}"
        )


@allure.title("Get all eco news with title")
@allure.description("""
    This test checks the response of the request to get all eco news with title.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Eco News")
@allure.feature("Get all eco news")
@allure.story("Get all eco news with title")
@allure.tag("Eco News")
@pytest.mark.parametrize(
    "expected_size, title",
    DataProvider.get_data("test_get_all_eco_news_with_title")
)
def test_get_all_eco_news_with_title(expected_size, title):
    api = BaseApi(f"{Data.BASE_URL}eco-news")
    actual_response = api.get_data(query_params={"title": title})
    assert actual_response.status_code == HTTPStatus.OK
    actual_json_response = actual_response.json()
    assert actual_json_response["totalElements"] == expected_size, (
        f"Expected {expected_size} news, but got {actual_json_response["totalElements"]}"
    )
    for news in actual_json_response["page"]:
        assert "title" in news, (
            f"Expected 'title' key in news, but got {news}"
        )
        assert title.lower() in news["title"].lower(), (
            f"Expected title {title}, but got {news['title']}"
        )


@allure.title("Get all eco news with author id")
@allure.description("""
    This test checks the response of the request to get all eco news with author id.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Eco News")
@allure.feature("Get all eco news")
@allure.story("Get all eco news with author id")
@allure.tag("Eco News")
@pytest.mark.parametrize(
    "expected_size, author_id",
    DataProvider.get_data("test_get_all_eco_news_with_author_id")
)
def test_get_all_eco_news_with_author_id(expected_size, author_id):
    api = BaseApi(f"{Data.BASE_URL}eco-news")
    actual_response = api.get_data(query_params={"author-id": author_id})
    assert actual_response.status_code == HTTPStatus.OK, (
        f"Expected status code 200, but got {actual_response.status_code}"
    )
    actual_json_response = actual_response.json()
    assert actual_json_response["totalElements"] == expected_size, (
        f"Expected {expected_size} news, but got {len(actual_json_response['page'])}"
    )
    for news in actual_json_response["page"]:
        assert "author" in news, (
            f"Expected 'author' key in news, but got {news}"
        )
        assert news["author"]["id"] == author_id, (
            f"Expected author id {author_id}, but got {news['author']['id']}"
        )


@allure.title("Get all eco news with pagination")
@allure.description("""
    This test checks the response of the request to get all eco news with pagination.
                    """)
@allure.severity(allure.severity_level.NORMAL)
@allure.epic("Eco News")
@allure.feature("Get all eco news")
@allure.story("Get all eco news with pagination")
@allure.tag("Eco News")
@pytest.mark.parametrize(
    "expected_size, page, size",
    DataProvider.get_data("test_get_all_eco_news_with_pagination")
)
def test_get_all_eco_news_with_pagination(expected_size, page, size):
    api = BaseApi(f"{Data.BASE_URL}eco-news")
    actual_response = api.get_data(query_params={"page": page, "size": size})
    assert actual_response.status_code == HTTPStatus.OK, (
        f"Expected status code 200, but got {actual_response.status_code}"
    )
    actual_json_response = actual_response.json()
    assert len(actual_json_response["page"]) == expected_size, (
        f"Expected {expected_size} news, but got {len(actual_json_response['page'])}"
    )
