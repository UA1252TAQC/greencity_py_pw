import json
import os


class DataProvider:
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
        return data[test_method]
        # test_cases = self._data_ui
        # for i in range(len(test_cases)):
        #     for j in range(len(test_cases[i])):
        #         test_cases[i][j] = self.handle_special_cell(test_cases[i][j])
        #  test_cases

    def handle_special_cell(self, cell):
        if cell is None or cell == "null":
            return None

        special_cases = {
            # "GENERATE_TEMPORARY_EMAIL": lambda: self.mail_utils.create_inbox()["id"],
            "EXTRACT_GOOGLE_EMAIL": lambda: os.getenv("GOOGLE_EMAIL"),
            "EXTRACT_GOOGLE_PASSWORD": lambda: os.getenv("GOOGLE_PASSWORD"),
            "EXTRACT_GOOGLE_NAME": lambda: os.getenv("GOOGLE_NAME")
        }

        return special_cases.get(cell, lambda: cell)()


if __name__ == "__main__":
    print(DataProvider.get_ui_test_data("testUsernameValidation"))
