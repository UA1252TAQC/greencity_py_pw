"""
This module provides utility functions to facilitate API communication for the habit-related features
of the application. It includes methods to prepare request headers, retrieve a list of habits,
and handle API errors.

Functions:
    - prepare_headers(auth_token): Prepares headers for authenticated API requests.
    - get_habit_list(api_url, headers): Retrieves a list of habits from the specified API.
    - handle_api_error(response, message): Logs and raises an exception if an API request fails.
"""
import logging as log

from api.base_api import BaseApi


def prepare_headers(auth_token):
    """
    Prepares the headers required for making authenticated API requests.

    :param auth_token: The authentication token used for accessing the API.
    :return: A dictionary containing the necessary headers for the request.
    """
    return {
        'accept': '*/*',
        'Authorization': f"Bearer {auth_token}"
    }


def get_habit_list(api_url, headers):
    """
    Send a GET request to retrieve a list of habits.
    """
    api = BaseApi(api_url)
    response = api.get_data(headers=headers)

    if response.status_code == 200:
        log.info("CONFTEST: Successfully retrieved habit list.")
        return response.json().get('page', [])
    else:
        handle_api_error(response, "Failed to retrieve habit list")


def handle_api_error(response, message):
    """
        Handles errors that occur during an API request by logging the error and raising an exception.

        :param response: The response object returned from the API call.
        :param message: A custom error message to log if the API request fails.
        :raises HTTPError: This will raise an HTTPError with the appropriate status code and message.
        """
    log.error(f"CONFTEST: {message}. Status code: {response.status_code}")
    response.raise_for_status()
