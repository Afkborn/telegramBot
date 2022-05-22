
from os import getcwd
import sqlite3 as sql # sqlite3 is a module

from python.Model.User import User



CREATETABLE_USERS = f"""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER ,
    is_bot INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    created_at INTEGER
);"""


class Database():
    dbName = "database.db"
    dbLoc = fr"db/{dbName}"
    
    def __init__(self) -> None:
        self.createDB()
    
    def createDB(self):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(CREATETABLE_USERS)
        self.db.commit()
        self.db.close()


    def addUser(self,user:User):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"telegram_id,is_bot,username,first_name,last_name,language_code,created_at"
        VALUES = f"""
        '{user.get_telegram_id()}',
        '{user.get_is_bot()}',
        '{user.get_username()}',
        '{user.get_first_name()}',
        '{user.get_last_name()}',
        '{user.get_language_code()}',
        '{user.get_created_at()}'
        """
        self.im.execute(f"INSERT INTO users ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()
        

    def addUserIfNotExists(self,user:User):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM users WHERE username = '{user.get_username()}'")
        result = self.im.fetchone()
        if result != None:
            return False
        self.addUser(user)
        self.db.close()
        return True
    
    def getUserWithUsername(self, username:str) -> User:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM users WHERE username = '{username}'")
        result = self.im.fetchone()
        print(result)
        if result == None:
            return None
        id,telegram_id, is_bot, username, first_name, last_name, language_code, created_at = result
        user = User(id=id,telegram_id=telegram_id,is_bot=is_bot,username=username,first_name=first_name,last_name=last_name,language_code=language_code,created_at=created_at)
        self.db.close()
        return user
    
    def getUserWithTelegramID(self, telegram_id:int) -> User:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM users WHERE telegram_id = '{telegram_id}'")
        result = self.im.fetchone()
        if result == None:
            return None
        id,telegram_id, is_bot, username, first_name, last_name, language_code, created_at = result
        user = User(id=id,telegram_id=telegram_id,is_bot=is_bot,username=username,first_name=first_name,last_name=last_name,language_code=language_code,created_at=created_at)
        self.db.close()
        return user
    
    def getAllTelegramID(self) -> int:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute("SELECT telegram_id FROM users")
        result = self.im.fetchall()
        self.db.close()
        return result
    
        
    def getUserCount(self) -> int:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute("SELECT COUNT(*) FROM users")
        result = self.im.fetchone()
        self.db.close()
        return result[0]
    

    
    

    