import psycopg2
from typing import List, Dict, Any
from config import DB_CONFIG


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.connection.autocommit = True

    def execute(self, query: str, params: tuple = None) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

    def fetch(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def close(self):
        self.connection.close()


db = Database()
