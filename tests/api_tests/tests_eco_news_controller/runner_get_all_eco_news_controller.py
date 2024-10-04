import pytest


from api.base_api import BaseApi

class RunnerGetAllEcoNews:

    @pytest.fixture
    def setup_method(self):
        self.api = BaseApi('https://greencity.greencity.cx.ua/eco-news')