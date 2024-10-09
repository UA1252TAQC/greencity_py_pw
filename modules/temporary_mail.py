import os
import requests
from datetime import datetime, timedelta
from typing import List
from requests.exceptions import HTTPError


class MailUtils:
    def __init__(self):
        self.base_url = os.getenv("MAILSLURP_BASE_URL")
        self.api_key = os.getenv("MAILSLURP_API_KEY")
        print(self.base_url, self.api_key)
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_all_inboxes(self) -> List[dict]:
        try:
            response = requests.get(f"{self.base_url}/inboxes", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise RuntimeError(f"Other error occurred: {err}")

    def create_inbox(self) -> dict:
        expiration = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
        payload = {"expiresAt": expiration}

        try:
            response = requests.post(f"{self.base_url}/inboxes", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise RuntimeError(f"Other error occurred: {err}")

    def get_last_mail(self, inbox_id: str, timeout_millis: int) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}/waitForLatestEmail",
                headers=self.headers,
                params={"inboxId": inbox_id, "timeout": timeout_millis}
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            raise RuntimeError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise RuntimeError(f"Other error occurred: {err}")


if __name__ == "__main__":
    mail_utils = MailUtils()
    print(mail_utils.create_inbox())
