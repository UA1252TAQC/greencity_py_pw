import json
from typing import Callable, Iterator, Tuple, Any
from modules.mail_utils import MailUtils


class DataProvider:
    _data = None
    mail_utils = MailUtils()

    def __init__(self, json_file: str):
        self.json_file = json_file
        self.load_data()

    def load_data(self):
        if DataProvider._data is None:
            with open(self.json_file) as file:
                DataProvider._data = json.load(file)

    def get_test_cases(self, method: Callable) -> Iterator[Tuple]:
        data_type = method.__name__.replace("dp", "")
        data_nodes = DataProvider._data.get(data_type, [])
        for node in data_nodes:
            yield self.parse_row(node, method)

    def parse_row(self, node: Any, method: Callable) -> Tuple:
        parameter_types = method.__annotations__.values()
        row = []
        for i, param_type in enumerate(parameter_types):
            cell = node[i] if i < len(node) else None
            row.append(self.convert_json_to_type(cell, param_type))
        return tuple(row)

    def convert_json_to_type(self, cell: Any, expected_type: Any) -> Any:
        if cell is None or cell == "null":
            return None

        if cell == "GENERATE_TEMPORARY_EMAIL":
            return self.mail_utils.create_inbox().get("id")
        elif cell == "EXTRACT_GOOGLE_EMAIL":
            return self.config_properties.get_google_email()
        elif cell == "EXTRACT_GOOGLE_PASSWORD":
            return self.config_properties.get_google_password()
        elif cell == "EXTRACT_GOOGLE_NAME":
            return self.config_properties.get_google_name()

        if expected_type == str:
            return str(cell)
        elif expected_type == bool:
            return bool(cell)
        elif expected_type == int:
            return int(cell)
        elif expected_type == float:
            return float(cell)
        else:
            return str(cell)
