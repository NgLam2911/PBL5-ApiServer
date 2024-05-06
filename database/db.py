import database
from pymongo import MongoClient
from config import Config
from utilties import Singleton

class Database(Singleton):
    config = Config()
    def __init__(self):
        pass
    
    # All time format is in UNIX timestamp (int)
    
    def connect(self) -> MongoClient:
        return MongoClient(self.config.db_host(),
                           username=self.config.db_auth_user(),
                           password=self.config.db_auth_password(),
                           authSource=self.config.db_auth_source())
        
    def insert_sensor_data(self, time: int, food_weight: float, water_weight: float):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["sensor-data"]
            return col.insert_one({'time': time, 'food_weight': food_weight, 'water_weight': water_weight})
        
    def get_sensor_data(self, time=None, from_time=None, to_time=None):
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
    
    def delete_sensor_data(self, time=None, from_time=None, to_time=None):
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
            
    def insert_image_data(self, time: int, uuid: str, amg: str):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["image-data"]
            return col.insert_one({'time': time, 'uuid': uuid, 'amg': amg})
        
    def get_image_data(self, time=None, from_time=None, to_time=None):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["image-data"]
            if time:
                return col.find_one({'time': time})
            elif from_time:
                if to_time:
                    return col.find({'time': {'$gte': from_time, '$lte': to_time}})
                else:
                    return col.find({'time': {'$gte': from_time}})
            else:
                return col.find()
            
    def get_image_data_by_uuid(self, uuid: str):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["image-data"]
            return col.find_one({'uuid': uuid})
        
            
    def insert_last_uuid(self, uuid: str):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["last-uuid"]
            return col.insert_one({'uuid': uuid})
        
    def get_last_uuid(self):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["last-uuid"]
            return col.find_one()
        
    def update_last_uuid(self, uuid: str):
        with self.connect() as client:
            db = client[self.config.db_name()]
            col = db["last-uuid"]
            return col.update_one({}, {'$set': {'uuid': uuid}})
        
    
    # Useable functions
    
    def addSensorData(self, time: int, food_weight: float, water_weight: float):
        return self.insert_sensor_data(time, food_weight, water_weight)
    
    def getSensorData(self, time=None, from_time=None, to_time=None):
        query = self.get_sensor_data(time, from_time, to_time)
        result = []
        for i in query:
            result.append({
                'time': i['time'],
                'food_weight': i['food_weight'],
                'water_weight': i['water_weight']
            })
        return result
    
    def deleteSensorData(self, time=None, from_time=None, to_time=None):
        return self.delete_sensor_data(time, from_time, to_time)
    
    def addImageData(self, time: int, uuid: int, amg: str):
        return self.insert_image_data(time, uuid, amg)
    
    def getImageData(self, time=None, from_time=None, to_time=None):
        query = self.get_image_data(time, from_time, to_time)
        result = []
        for i in query:
            result.append({
                'time': i['time'],
                'uuid': i['uuid'],
                'amg': i['amg']
            })
        return result
    
    def getImageDataByUUID(self, uuid: str):
        query = self.get_image_data_by_uuid(uuid)
        result = {
            'time': query['time'],
            'uuid': query['uuid'],
            'amg': query['amg']
        }
        return result
    
    def setLastUUID(self, uuid: str):
        if self.get_last_uuid():
            return self.update_last_uuid(uuid)
        else:
            return self.insert_last_uuid(uuid)
        
    def getLastUUID(self) -> str:
        query = self.get_last_uuid()
        if query:
            return query['uuid']
        else:
            return '0'
        
    
        
    
        