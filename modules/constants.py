import os
from dotenv import load_dotenv


class Data:
    """
    Data class to store all the constants loaded from a .env file
    """
    load_dotenv()
    BASE_URL = os.getenv('BASE_URL')
    USER_BASE_URL = os.getenv('USER_BASE_URL')
    USER_ID = int(os.getenv('USER_ID'))
    USER_NAME = os.getenv('USER_NAME')
    USER_EMAIL = os.getenv('USER_EMAIL')
    USER_PASSWORD = os.getenv('USER_PASSWORD')
