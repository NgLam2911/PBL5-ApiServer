import database
import sqlite3
import os
from config import Config
from utilties import Singleton

class Database(Singleton):
    # Requests from flask is already async, so we don't need to worry about async here
    config = Config()
    
    def __init__(self):
        if not os.path.exists(self.config.db_path()):
            with sqlite3.connect(self.config.db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute(database.db_stmt.init_table())
                print("Database initialized")
                conn.commit()
        
    def insert_data(self, time: int, data: str):
        with sqlite3.connect(self.config.db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(database.db_stmt.insert_data(time, data))
            conn.commit()
        
    def get_data(self, time=None, from_time=None, to_time=None):
        with sqlite3.connect(self.config.db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(database.db_stmt.get_data(time, from_time, to_time))
            return cursor.fetchall()
    
    def delete_data(self, time=None, from_time=None, to_time=None):
        with sqlite3.connect(self.config.db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute(database.db_stmt.delete_data(time, from_time, to_time))
            conn.commit()
        