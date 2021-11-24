# performing important imports
from datetime import datetime


class AppLogger:
    @staticmethod
    def log(file_object, log_message, level=''):
        now = datetime.now()
        date = str(now.date())
        current_time = now.strftime('%H:%M:%S')
        file_object.write(
            str(date) + '/' + str(current_time) + ': ' + str(level) + ' :: ' + '\t\t' + log_message + '\n'
        )
