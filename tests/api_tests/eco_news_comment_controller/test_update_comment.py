from http import HTTPStatus

import logging as log

import allure
import pytest

from api.base_api import BaseApi
from modules.constants import Data


@pytest.mark.comment
@allure.feature('Update Comment Feature')
@allure.story('Update comment in Eco News')
@allure.severity(allure.severity_level.NORMAL)
def test_update_comment_success(tc_logger,
                                get_auth_token,
                                setup_and_teardown_news,
                                setup_comment,
                                generate_comment_text_with_timestamp):
    try:
        test_name = "Verify successful updating of an existing comment on news."
        tc_logger.log_test_name(test_name)
        log.info(f"Test '{test_name}' started")

        comment_id = setup_comment.json()['id']
        modified_comment_text = generate_comment_text_with_timestamp

        log.info(f"Starting test {test_name}")
        api = BaseApi(
            f'{Data.API_BASE_URL}/econews/comments?id={comment_id}&text={modified_comment_text}'
        )
        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {get_auth_token}'
        }
        data = modified_comment_text
        response = api.patch_data(headers=headers, payload=data)
        log.info(f"Response status code: {response.status_code}")

        assert response.status_code == HTTPStatus.OK
        log.info(f"Comment with ID {comment_id} updated successfully.")

    except Exception as e:
        log.error(f"An error occurred: {str(e)}")
        pytest.fail(f"Test failed due to an unexpected error: {str(e)}")
