import json
from pathlib import Path
from typing import Dict


class LocalizationUtils:
    def __init__(self, file_path: str = "localization.json"):
        self.file_path = Path(file_path)
        self.root_node = self._load_json()

    def _load_json(self) -> Dict:
        with self.file_path.open(encoding='utf-8') as f:
            return json.load(f)

    def get_form_messages(self, language: str) -> Dict[str, str]:
        localized_messages = {}
        form_node = self.root_node.get("form", {}).get(language, {})

        for key, message in form_node.items():
            localized_messages[key] = message

        return localized_messages
