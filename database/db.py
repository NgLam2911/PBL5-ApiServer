import database
from pymongo import MongoClient
from config import Config
from utilties import Singleton

class Database(Singleton):
    config = Config()
    def __init__(self):
        pass
    
    def connect(self) -> MongoClient:
        return MongoClient(self.config.db_host(),
                           username=self.config.db_auth_user(),
                           password=self.config.db_auth_password(),
                           authSource=self.config.db_auth_source())
        
    def insert_data(self, time: int, data: str):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["sensor-data"]
            col.insert_one({'time': time, 'data': data})
        
    def get_data(self, time=None, from_time=None, to_time=None):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["sensor-data"]
            if time:
                return col.find_one({'time': time})
            elif from_time:
                if to_time:
                    return col.find({'time': {'$gte': from_time, '$lte': to_time}})
                else:
                    return col.find({'time': {'$gte': from_time}})
            else:
                return col.find()
    
    def delete_data(self, time=None, from_time=None, to_time=None):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["sensor-data"]
            if time:
                return col.delete_one({'time': time})
            elif from_time:
                if to_time:
                    return col.delete_many({'time': {'$gte': from_time, '$lte': to_time}})
                else:
                    return col.delete_many({'time': {'$gte': from_time}})
            else:
                return col.delete_many({})
        