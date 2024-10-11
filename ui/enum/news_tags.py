from enum import Enum


class NewsTags(Enum):
    NEWS = ("News", "Новини")
    EVENTS = ("Events", "Події")
    EDUCATION = ("Education", "Освіта")
    INITIATIVES = ("Initiatives", "Ініціативи")
    ADS = ("Ads", "Реклама")

    def __init__(self, english_text, ukrainian_text):
        self.english_text = english_text
        self.ukrainian_text = ukrainian_text
        self.key = english_text

    def get_text(self, language_code: str) -> str:
        return self.ukrainian_text if language_code == 'ua' else self.english_text

    def get_tag_key(self) -> str:
        return self.key

    @staticmethod
    def get_all_tag_names() -> list:
        return list(NewsTags)
