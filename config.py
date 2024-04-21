import json
from utilties import Singleton

class Config(Singleton):
    
    def __init__(self):
        config_file = "config.json"
        if not hasattr(self, 'config'):
            with open(config_file) as f:
                self.config = json.load(f)
                self.hostnamev = self.config['hostname']
                self.model_pathv = self.config['model_path']
                self.model_typev = self.config['model_type']
                self.model_namev = self.config['model_name']
                self.image_pathv = self.config['image_path']
                self.predict_pathv = self.config['predict_path']
                self.db_pathv = self.config['db_path']
                self.last_uuid_pathv = self.config['last_uuid_path']
                
    def hostname(self):
        return self.hostnamev
    
    def model_path(self):
        return self.model_pathv
    
    def model_type(self):
        return self.model_typev
    
    def model_name(self):
        return self.model_namev
    
    def image_path(self):
        return self.image_pathv
    
    def predict_path(self):
        return self.predict_pathv
    
    def db_path(self):
        return self.db_pathv
    
    def last_uuid_path(self):
        return self.last_uuid_pathv
    
    
    
            