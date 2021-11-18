import pymongo
from configparser import ConfigParser


class DataBase:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config/config.ini')
        self.config.sections()
        self.session = None
        self.database = None
        self.collection = None

    def connect_db(self):
        """
        Connecting to the database
        """
        try:
            self.session = pymongo.MongoClient(self.config['Database']['connection_string'])
            self.database = self.session["Background_Removal"]
        except Exception as e:
            raise e

    def insert_data(self, collection_name, date, time, message, level):
        """

        :param collection_name: name of the respective collection
        :param date: current date
        :param time: current time
        :param message: log message to insert
        :param level: level of severity
                Info, Error, Warning
        """

        try:
            if self.is_connected():
                self.collection = self.database[collection_name]
                query = {
                    "cur_date": date,
                    "cur_time": time,
                    "level": level,
                    "message": message
                }
                self.collection.insert_one(query)
            else:
                raise Exception('Database not connected')
        except Exception as e:
            raise e

    def read_data(self, collection_name):
        """
        Read data from database
        :param collection_name: name of collection to access
        :return: retrieved data
        """

        try:
            if self.is_connected():
                self.collection = self.database[collection_name]
                data = self.collection.find({}).sort("cur_date").sort("time_cur")
            else:
                raise Exception('Database not connected')
            return data
        except Exception as e:
            raise e

    def is_connected(self):
        """
        Check is database is connected
        :return: True- Connected
                 False- Not Connected
        """

        try:
            if self.session is not None:
                return True
            else:
                return False
        except Exception as e:
            raise e
