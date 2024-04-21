import json
from config import Config


def check_file(file):
    if file.filename == '':
        return {'message': 'No file selected'}, 400
    if file and file.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        return {'message': 'Invalid file format'}, 400
    return None

def setLastUUID(uuid: str):
    config = Config()
    with open(config.last_uuid_path(), 'w') as f:
        json.dump({'last': uuid}, f)
        
def getLastUUID() -> str:
    config = Config()
    try:
        with open(config.last_uuid_path, 'r') as f:
            data = json.load(f)
            return data['last']
    except:
        return '0'
    
def db_data_to_json(raw_data):
    # raw_data from the database is a list of tuples
    result = []
    for row in raw_data:
        json_data = json.loads(row[1])
        food_weight = json_data['food_weight']
        time = row[0]
        result.append({'time': time, 'food_weight': food_weight})
    return result