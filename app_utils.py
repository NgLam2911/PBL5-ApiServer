import json

def check_file(file):
    if file.filename == '':
        return {'message': 'No file selected'}, 400
    if file and file.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        return {'message': 'Invalid file format'}, 400
    return None

def setLastUUID(uuid: str):
    with open('last.json', 'w') as f:
        json.dump({'last': uuid}, f)
        
def getLastUUID() -> str:
    try:
        with open('last.json', 'r') as f:
            data = json.load(f)
            return data['last']
    except:
        return '0'
    
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance