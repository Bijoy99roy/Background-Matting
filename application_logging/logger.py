# performing important imports
from datetime import datetime
from db_operations.database import DataBase


class AppLogger:
    def __init__(self):
        self.database = DataBase()

    def log(self, collection_name, message, level=''):
        now = datetime.now()
        date = str(now.date())
        current_time = now.strftime('%H:%M:%S')
        self.database.insert_data(collection_name, date, current_time, message, level)
