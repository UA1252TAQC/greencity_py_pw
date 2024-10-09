import json


class DataProvider:
    _data = None

    @staticmethod
    def get_data(key):
        if (DataProvider._data is None):
            with open('test_data_api.json') as file:
                DataProvider._data = json.load(file)
        return DataProvider._data[key]
