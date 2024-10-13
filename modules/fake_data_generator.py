from faker import Faker
import random
from typing import List

from ui.enum.news_tags import NewsTags

fake = Faker()


def generate_news_data():
    title = fake.sentence(nb_words=10)
    content = fake.paragraph(nb_sentences=100)
    tags = generate_random_tags()
    return title, content, tags


def generate_random_tags() -> List[NewsTags]:
    return random.sample(list(NewsTags), random.randint(1, len(NewsTags)))
