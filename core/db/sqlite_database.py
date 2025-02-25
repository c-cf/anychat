import sqlite3
from core.db.base import DatabaseInterface

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    async def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    async def disconnect(self):
        if self.connection:
            self.connection.close()

    async def execute(self, query: str, params: dict = None):
        if not self.connection:
            raise Exception("Database not connected")
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()
