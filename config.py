import json
from utilties import Singleton

class Config(Singleton):
    
    def __init__(self):
        config_file = "data/config.json"
        if not hasattr(self, 'config'):
            # Check if the config file exists, if not create one
            try: 
                with open(config_file) as f:
                    self.config = json.load(f)
                    self.hostnamev = self.config['hostname']
                    self.model_pathv = self.config['model_path']
                    self.model_typev = self.config['model_type']
                    self.model_namev = self.config['model_name']
                    self.image_pathv = self.config['image_path']
                    self.predict_pathv = self.config['predict_path']
                    self.db_hostv = self.config['database']['host']
                    self.db_namev = self.config['database']['db']
                    self.db_auth_userv = self.config['database']['auth']['user']
                    self.db_auth_passwordv = self.config['database']['auth']['password']
                    self.db_auth_sourcev = self.config['database']['auth']['authSource']
            except:
                self.hostnamev = "localhost:5000"
                self.model_pathv = "yolov5s.pt"
                self.model_typev = "ultralytics/yolo"
                self.model_namev = "yolov5s"
                self.image_pathv = "data/images"
                self.predict_pathv = "data/predict"
                self.databasev = "data/db"
                self.last_uuid_pathv = "data/last_uuid"
                self.db_hostv = 'mongodb://localhost:27017/'
                self.db_namev = "pbl5"
                self.db_auth_userv = "admin"
                self.db_auth_passwordv = "123456789"
                self.db_auth_sourcev = "admin"
                self.config = {
                    "hostname": self.hostnamev,
                    "model_path": self.model_pathv,
                    "model_type": self.model_typev,
                    "model_name": self.model_namev,
                    "image_path": self.image_pathv,
                    "predict_path": self.predict_pathv,
                    "database": {
                        "host": self.db_hostv,
                        "db": self.db_namev,
                        "auth": {
                            "user": self.db_auth_userv,
                            "password": self.db_auth_passwordv,
                            "authSource": self.db_auth_sourcev
                        }
                    }
                }
                with open(config_file, 'w') as f:
                    json.dump(self.config, f, indent=4)
                
                
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
    
    def db_host(self):
        return self.db_hostv
    
    def db_name(self):
        return self.db_namev
    
    def db_auth_user(self):
        return self.db_auth_userv
    
    def db_auth_password(self):
        return self.db_auth_passwordv
    
    def db_auth_source(self):
        return self.db_auth_sourcev
    
    
    
            