from api.base_api import BaseApi
from http import HTTPStatus


def test_get_eco_news_default():
    api = BaseApi('https://greencity.greencity.cx.ua/eco-news')
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


def test_get_eco_news_with_tags():
    api = BaseApi('https://greencity.greencity.cx.ua/eco-news')
    params = {"tags": ["News", "Education"]}
    response = api.get_data(query_params=params)
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


def test_get_eco_news_with_title():
    api = BaseApi('https://greencity.greencity.cx.ua/eco-news')
    params = {"title": "Plant trees"}
    response = api.get_data(query_params=params)
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


def test_get_eco_news_with_author_id():
    api = BaseApi('https://greencity.greencity.cx.ua/eco-news')
    params = {"author-id": 19}
    response = api.get_data(query_params=params)
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


def test_get_eco_news_with_pagination():
    api = BaseApi('https://greencity.greencity.cx.ua/eco-news')
    params = {"page": 0, "size": 5}
    response = api.get_data(query_params=params)
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
