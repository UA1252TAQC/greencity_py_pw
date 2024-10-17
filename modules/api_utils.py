"""
Utility functions for handling API requests in the application.
This file includes helper methods for POST, DELETE, and other common API interactions.
"""
from api.base_api import BaseApi


def post_data(api_url, headers):
    """
    Send a POST request to the given API.

    :param api_url: The API endpoint to send the POST request to.
    :param headers: The headers required for making the POST request (including authorization).
    :return: The response object from the POST request.
    """
    api = BaseApi(api_url)
    response = api.post_data(headers=headers)
    return response


def delete_data(api_url, headers):
    """
    Send a DELETE request to the given API.

    :param api_url: The API endpoint to send the DELETE request to.
    :param headers: The headers required for making the DELETE request (including authorization).
    :return: The response object from the DELETE request.
    """
    api = BaseApi(api_url)
    response = api.delete_data(headers=headers)
    return response


def get_data(api_url, headers):
    """
    Send a GET request to the given API.

    :param api_url: The API endpoint to send the GET request to.
    :param headers: The headers required for making the GET request (including authorization).
    :return: The response object from the GET request.
    """
    api = BaseApi(api_url)
    response = api.get_data(headers=headers)
    return response
