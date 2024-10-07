import os
import psycopg2
from dotenv import load_dotenv


class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.connection = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT')
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            print(f"An error occurred: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.connection.close()
