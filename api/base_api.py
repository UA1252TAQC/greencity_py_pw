"""
Module that represents base api functionality
"""

from typing import Dict, Optional, Any

import requests
import logging as log
from requests import Response


class BaseApi:
    """
    Class that represents base api functionality
    """
    response = Response

    def __init__(self, url: str):
        self._url = url

    def get_data(
        self,
        headers: Dict[str, str] = None,
        query_params: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Response:
        """
        Method that makes GET request to the specified url
        :param headers: headers for the request
        :param query_params: query parameters for the request
        :param kwargs: additional arguments for the request
        :return: response from the request
        """
        try:
            response = requests.get(
                self._url, params=query_params, headers=headers, **kwargs
            )
            log.info(f"API: Making GET request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: GET request failed: {error}")
            response = None

        return response

    def post_data(
        self, payload: Any = None, headers: Dict[str, str] = None, **kwargs
    ) -> Response:
        """
        Method that makes POST request to the specified url
        :param payload: data for the request
        :param headers: headers for the request
        :param kwargs: additional arguments for the request
        :return: response from the request
        """
        try:
            response = requests.post(self._url, json=payload, headers=headers, **kwargs)
            log.info(f"API: Making POST request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: POST request failed: {error}")
            response = None

        return response

    def put_data(
        self, payload: Any = None, headers: Dict[str, str] = None, **kwargs
    ) -> Response:
        """ 
        Method that makes PUT request to the specified url
        :param payload: data for the request
        :param headers: headers for the request
        :param kwargs: additional arguments for the request
        :return: response from the request
        """
        try:
            response = requests.put(self._url, json=payload, headers=headers, **kwargs)
            log.info(f"API: Making PUT request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: PUT request failed: {error}")
            response = None

        return response

    def delete_data(
        self, headers: Dict[str, str] = None, payload: Any = None
    ) -> Response:
        """
        Method that makes DELETE request to the specified url
        :param headers: headers for the request
        :param payload: data for the request
        :return: response from the request
        """

        try:
            response = requests.delete(self._url, headers=headers, json=payload)
            log.info(f"API: Making DELETE request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: DELETE request failed: {error}")
            response = None
        return response


    def patch_data(
        self, payload: Any = None, headers: Dict[str, str] = None, **kwargs
    ) -> Response:
        """
        Method that makes PATCH request to the specified url
        :param payload: data for the request
        :param headers: headers for the request
        :param kwargs: additional arguments for the request
        :return: response from the request
        """
        try:
            response = requests.patch(self._url, json=payload, headers=headers, **kwargs)
            log.info(f"API: Making PATCH request to {self._url}.")
        except requests.exceptions.RequestException as error:
            log.error(f"API: PATCH request failed: {error}")
            response = None

        return response
