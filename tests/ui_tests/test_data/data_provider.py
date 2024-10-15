from tests.ui_tests.test_data.test_data import test_data


def data_provider(key: str):
    data_item = test_data.get(key, {})
    return tuple(data_item.values())
