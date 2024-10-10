import json
import os

from modules.mail_utils import MailUtils


class DataProvider:
    mail_utils = MailUtils()

    @staticmethod
    def load_data(path):
        with open(path) as file:
            return json.load(file)

    @staticmethod
    def get_api_test_data(test_method):
        data = DataProvider.load_data('test_data_api.json')
        return data[test_method]

    @staticmethod
    def get_ui_test_data(test_method):
        data = DataProvider.load_data('test_data_ui.json')
        required_data = data[test_method]
        for i in range(len(required_data)):
            for j in range(len(required_data[i])):
                required_data[i][j] = DataProvider().handle_special_cell(required_data[i][j])
        return required_data

    def handle_special_cell(self, cell):
        if cell is None or cell == "null":
            return None

        special_cases = {
            "GENERATE_TEMPORARY_EMAIL": lambda: DataProvider.mail_utils.create_inbox(),
            "EXTRACT_GOOGLE_EMAIL": lambda: os.getenv("GOOGLE_EMAIL"),
            "EXTRACT_GOOGLE_PASSWORD": lambda: os.getenv("GOOGLE_PASSWORD"),
            "EXTRACT_GOOGLE_NAME": lambda: os.getenv("GOOGLE_NAME")
        }

        return special_cases.get(cell, lambda: cell)()
