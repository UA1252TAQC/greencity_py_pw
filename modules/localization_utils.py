import json
from pathlib import Path
from typing import Dict


class LocalizationUtils:
    _data = None

    def __init__(self, file_path: str = "localization.json", language: str = "Ua"):
        self.file_path = Path(file_path)
        self._load_json()
        self.language = language

    def _load_json(self):
        if self._data is None:
            with self.file_path.open(encoding='utf-8') as f:
                self._data = json.load(f)

    def get_form_message(self, message):
        if message is None:
            return None
        return self._data["form"][self.language][message]