
from matplotlib.patches import FancyArrow
from .global_variables import *
from os import path, makedirs

import logging

def createFolder():
    for folder in FOLDERS_NAME:
        if not path.exists(folder):
            makedirs(folder)    
            logging.info("Created folder: " + folder)



def checkCompatibility():
    try:
        import telegram
    except ImportError:
        print("Telegram Library is not installed. Please install it.")
        logging.error("Telegram Library is not installed. Please install it.")
        return False
    
    try:
        import playwright
    except ImportError:
        print("playwright Library is not installed. Please install it.")
        logging.error("playwright Library is not installed. Please install it.")
        return False
    
    createFolder()
    return True
        