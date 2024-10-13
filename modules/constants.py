import os
from dotenv import load_dotenv


class Data:
    """
    Data class to store all the constants loaded from a .env file
    """
    load_dotenv()
    API_BASE_URL = os.getenv('API_BASE_URL')
    USER_API_BASE_URL = os.getenv('USER_API_BASE_URL')
    USER_ID = int(os.getenv('USER_ID'))
    USER_NAME = os.getenv('USER_NAME')
    USER_EMAIL = os.getenv('USER_EMAIL')
    USER_PASSWORD = os.getenv('USER_PASSWORD')

    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_PORT = int(os.getenv('DATABASE_PORT'))

    GOOGLE_NAME = os.getenv('GOOGLE_NAME')
    GOOGLE_EMAIL = os.getenv('GOOGLE_EMAIL')
    GOOGLE_PASSWORD = os.getenv('GOOGLE_PASSWORD')

    MAILSLURP_BASE_URL = os.getenv('MAILSLURP_BASE_URL')
    MAILSLURP_API_KEY = os.getenv('MAILSLURP_API_KEY')

    UI_BASE_URL = os.getenv('UI_BASE_URL')
    UI_GREEN_CITY_HOME_PAGE_URL = UI_BASE_URL + "/#/greenCity"
    UI_GREEN_CITY_NEWS_PAGE_URL = UI_BASE_URL + "/#/news"
    UI_GREEN_CITY_PROFILE_PAGE_URL = UI_BASE_URL + "/#/profile"


