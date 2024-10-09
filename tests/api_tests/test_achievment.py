from http import HTTPStatus

import pytest

from api.base_api import BaseApi
from modules.constants import Data


@pytest.mark.parametrize("achievementStatus, achievementCategoryId", [("ACHIEVED", 1), ("UNACHIEVED", 2)])
def test_achievements_by_type_and_category(tc_logger, get_auth_token, achievementStatus, achievementCategoryId):
    api = BaseApi(f'{Data.BASE_URL}/achievements')

    query_params = {"achievementStatus": achievementStatus,
                    "achievementCategoryId": achievementCategoryId}

    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {get_auth_token}',
        'Content-Type': 'application/json'
    }

    response = api.get_data(headers=headers, query_params=query_params)
    json_response = response.json()
    assert isinstance(json_response, list)
    achievements = dict(json_response[0])
    assert response.status_code == HTTPStatus.OK
    expected_keys = ['id', 'title', 'name', 'nameEng', 'achievementCategory', 'condition', 'progress']
    for expected_key in expected_keys:
        assert expected_key in achievements
    expected_achievement_categories = ['id', 'name']
    achievement_categories = achievements.get('achievementCategory')
    for expected_achievement_category in expected_achievement_categories:
        assert expected_achievement_category in achievement_categories