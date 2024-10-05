import pytest
from http import HTTPStatus

from tests.api_tests.tests_eco_news_controller.runner_get_all_eco_news_controller import RunnerGetAllEcoNews

@pytest.mark.usefixtures("setup_method")
class TestsGetAllEcoNews(RunnerGetAllEcoNews):

    def test_get_eco_news_default(self):
        response = self.api.get_data()
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

    def test_get_eco_news_with_tags(self):
        params = {"tags": ["News", "Education"]}
        response = self.api.get_data(query_params=params)
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

    def test_get_eco_news_with_title(self):
        params = {"title": "Plant trees"}
        response = self.api.get_data(query_params=params)
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

    def test_get_eco_news_with_author_id(self):
        params = {"author-id": 19}
        response = self.api.get_data(query_params=params)
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

    def test_get_eco_news_with_pagination(self):
        params = {"page": 0, "size": 5}
        response = self.api.get_data(query_params=params)
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
