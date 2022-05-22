from datetime import datetime

def get_time():
    return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

def get_time_command():
    return datetime.now().strftime("%H:%M:%S.%f")