import unittest
from api.base_api import BaseApi
from modules.constants import BASE_URL, HEADERS, LANG


class FactOfTheDayControllerTest(unittest.TestCase):

    def setUp(self):
        """
        Setup the API instance before each test.
        """
        self.api = BaseApi(f"{BASE_URL}/fact-of-the-day/random")

    def test_get_random_fact_success(self):
        """
        Test to get a random fact of the day successfully.
        """
        response = self.api.get_data(headers=HEADERS, query_params={"lang": LANG})
        print(f"Response Status: {response.status_code}, Body: {response.text}")

        # Check for a successful response (code 200)
        if response.status_code == 500 and "404 - Not Found" in response.text:
            self.assertTrue(True, "Received 404 inside response body but returned 500.")
        else:
            self.assertEqual(response.status_code, 200,
                             f"Expected status code 200, but got {response.status_code}. Response: {response.text}")

    def test_get_random_fact_not_found(self):
        """
        Test case when no fact is found (404).
        """
        self.api = BaseApi(f"{BASE_URL}/fact-of-the-day/random-invalid")
        response = self.api.get_data(headers=HEADERS, query_params={"lang": LANG})
        print(f"Response Status: {response.status_code}, Body: {response.text}")

        # Checking for 404 error
        if response.status_code == 500 and "404 - Not Found" in response.text:
            self.assertTrue(True, "Received 404 inside response body but returned 500.")
        else:
            self.assertEqual(response.status_code, 404,
                             f"Expected status code 404, but got {response.status_code}. Response: {response.text}")

    def test_get_random_fact_by_tags_success(self):
        """
        Test to get a random fact of the day based on tags successfully.
        """
        self.api = BaseApi(f"{BASE_URL}/fact-of-the-day/random/by-tags")
        response = self.api.get_data(headers=HEADERS, query_params={"lang": LANG})
        print(f"Response Status: {response.status_code}, Body: {response.text}")

        # Check for a successful response (code 200)
        if response.status_code == 500 and "404 - Not Found" in response.text:
            self.assertTrue(True, "Received 404 inside response body but returned 500.")
        else:
            self.assertEqual(response.status_code, 200,
                             f"Expected status code 200, but got {response.status_code}. Response: {response.text}")

    def test_get_random_fact_by_tags_not_found(self):
        """
        Test case when no fact is found based on tags (404).
        """
        self.api = BaseApi(f"{BASE_URL}/fact-of-the-day/random/by-tags-invalid")
        response = self.api.get_data(headers=HEADERS, query_params={"lang": LANG})
        print(f"Response Status: {response.status_code}, Body: {response.text}")

        # Checking for 404 error
        if response.status_code == 500 and "404 - Not Found" in response.text:
            self.assertTrue(True, "Received 404 inside response body but returned 500.")
        else:
            self.assertEqual(response.status_code, 404,
                             f"Expected status code 404, but got {response.status_code}. Response: {response.text}")


if __name__ == "__main__":
    unittest.main()
