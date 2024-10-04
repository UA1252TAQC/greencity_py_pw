"""
Module that represents base api functionality
"""
from typing import Dict, Optional, Any

import requests
import logging as log
from requests import Response


class BaseApi:
    """
    class that represents base api methods
    """
    response = Response

    def __init__(self, url: str):
        self._url = url

    def get_data(self,
                 headers: Dict[str, str] = None,
                 query_params: Optional[Dict[str, str]] = None,
                 **kwargs) -> Response:
        """
        get data by endpoints with data
        :http_method: type of http_method
        :headers: headers
        :querystring: params for query string
        :kwargs: kwargs (data, json, params, ...)
        :return: response

        :Example:

        The following example will show how use that http_method

        .. code-block:: python

            from api.base_api import BaseApi

            class User(BaseApi):

                def get_user_data(self, http_method, headers: dict = None,
                    querystring: dict = None, **kwargs) -> BaseApi.response:

                    log.info("Customer: Get response")

                    return self.get_data(http_method, headers, querystring,
                     **kwargs)
        """
        try:
            response = requests.get(self._url,
                                    params=query_params,
                                    headers=headers,
                                    **kwargs)
            log.info(f"API: Making GET request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: GET request failed: {error}")
            response = None

        return response

    def post_data(self,
                  payload: Any = None,
                  headers: Dict[str, str] = None,
                  **kwargs) -> Response:
        """
        post data to the endpoint
        :data: data to be sent in the body of the request
        :headers: headers
        :kwargs: kwargs (params, ...)
        :return: response
        """
        try:
            response = requests.post(self._url,
                                     json=payload,
                                     headers=headers,
                                     **kwargs)
            log.info(f"API: Making POST request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: POST request failed: {error}")
            response = None

        return response

    def put_data(self,
                 payload: Any = None,
                 headers: Dict[str, str] = None,
                 **kwargs) -> Response:
        """
        Make a PUT request with the specified data and headers.

        :param payload: The payload data to be sent (as a dictionary).
        :param headers: The headers to be included in the request.
        :param kwargs: Additional keyword arguments to be passed to the
        `requests.put()` function.
        :return: The response object.
        """
        try:
            response = requests.put(self._url,
                                    json=payload,
                                    headers=headers,
                                    **kwargs)
            log.info(f"API: Making PUT request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: PUT request failed: {error}")
            response = None

        return response

    def delete_data(self,
                    headers: Dict[str, str] = None,
                    payload: Any = None) -> Response:
        """
        Send DELETE request to delete some data

        :param payload:
        :param headers: headers

        :return: response

        :Example:

        The following example will show how use that http_method

        .. code-block:: python

            from api.base_api import BaseApi

            def some_test():
                test_id = 123
                url = Property.LOCATION_URL.format(test_id)
                test = BaseApi(url)
                test.delete_data()

        """
        try:
            response = requests.delete(self._url,
                                       headers=headers,
                                       json=payload)
            log.info(f"API: Making DELETE request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: DELETE request failed: {error}")
            response = None

        return response

    def patch_data(self,
                   payload: Any = None,
                   headers: Dict[str, str] = None,
                   **kwargs) -> Response:
        """
        Make PATCH request to update data.

        :param payload:
        :param headers: headers

        :return: response

        :Example:


        """
        try:
            response = requests.patch(self._url,
                                      json=payload,
                                      headers=headers,
                                      **kwargs)
            log.info(f"API: Making PATCH request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: PATCH request failed: {error}")
            response = None

        return response
