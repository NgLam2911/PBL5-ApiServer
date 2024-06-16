from pymongo import MongoClient
import datetime
import time as t

time = "2024-05-19 12:00:00"
food_weight = 100
water_weight = 100
actual_time = int(t.mktime(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S").timetuple()))


# DO NOT CHANGE
host = "mongodb://nglam.xyz:27017/"
user = "nglam2911"
pwd = "NgLam2911@Bruh"
source = "admin"
db_name = "pbl5-deploy"

db = MongoClient(host=host, username=user, password=pwd, authSource=source)

def add_sensor_data(time: int, food_weight: float, water_weight: float):
    col = db[db_name]["sensor-data"]
    if col.find_one({'time': time}):
        col.update_one({'time': time}, {'$set': {'food_weight': food_weight, 'water_weight': water_weight}})
    else:
        col.insert_one({'time': time, 'food_weight': food_weight, 'water_weight': water_weight})
        
add_sensor_data(actual_time, food_weight, water_weight)