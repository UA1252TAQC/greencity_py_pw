import os
import requests
from datetime import datetime, timedelta
from requests.exceptions import HTTPError


class MailUtils:
    def __init__(self):
        self.base_url = os.getenv("MAILSLURP_BASE_URL")
        self.api_key = os.getenv("MAILSLURP_API_KEY")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def create_inbox(self):
        expiration = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
        payload = {"expiresAt": expiration}

        try:
            response = requests.post(f"{self.base_url}inboxes", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise RuntimeError(f"Other error occurred: {err}")

    def get_last_mail(self, inbox_id: str):
        try:
            response = requests.get(
                f"{self.base_url}waitForLatestEmail",
                headers=self.headers,
                params={"inboxId": inbox_id, "timeout": 30000}
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise RuntimeError(f"Other error occurred: {err}")

    @staticmethod
    def extract_activation_link(body: str) -> str:
        start_token = '<div class="vertical-center"><a href="http'
        end_token = '" class="verify-email color-green-city'

        start_index = body.find(start_token)
        if start_index != -1:
            start_index += len(start_token) - 4
            end_index = body.find(end_token, start_index)

            if end_index == -1:
                end_index = body.find('"', start_index)

            if start_index < end_index:
                return body[start_index:end_index].replace('amp;', '')
        raise ValueError("Token cannot be parsed!")
