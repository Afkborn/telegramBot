
from os import getcwd
from re import S
import sqlite3 as sql # sqlite3 is a module

from python.Model.User import User
from python.Model.Product import Product


CREATETABLE_USERS = f"""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    is_bot INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    created_at INTEGER
);"""

CREATETABLE_URLS = f"""CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT
);"""

CREATETABLE_PRODUCT = """CREATE TABLE IF NOT EXISTS products (
    id	INTEGER PRIMARY KEY,
    owner_telegram_id INTEGER,
    isim TEXT NOT NULL,
    link TEXT NOT NULL,
    fiyat_takip TEXT NOT NULL, 
    stok_takip TEXT NOT NULL,
    fiyat INTEGER NOT NULL,
    stok TEXT NOT NULL,
    son_kontrol_zamani INTEGER NOT NULL,
    created_at INTEGER NOT NULL
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
        self.im.execute(CREATETABLE_URLS)
        self.im.execute(CREATETABLE_PRODUCT)
        self.db.commit()
        self.db.close()

    def addUrl(self, url: str):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"url"
        VALUES = f"'{url}'"
        self.im.execute(f"INSERT INTO urls ({KEY}) VALUES ({VALUES})")
        last_row_index = self.im.lastrowid
        self.db.commit()
        self.db.close()
        return last_row_index

    def getUrlIndex(self, index: int):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT url FROM urls WHERE id = {index}")
        result = self.im.fetchone()
        self.db.close()
        return result[0]
    
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
    
    def addProduct(self, product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"owner_telegram_id,isim,link,fiyat_takip,stok_takip,fiyat,stok,son_kontrol_zamani,created_at"
        VALUES = f"""
        '{product.get_owner_telegram_id()}',
        '{product.get_isim()}',
        '{product.get_link()}',
        '{product.get_fiyat_takip()}',
        '{product.get_stok_takip()}',
        '{product.get_fiyat()}',
        '{product.get_stok()}',
        '{product.get_son_kontrol_zamani()}',
        '{product.get_created_at()}'
        """
        self.im.execute(f"INSERT INTO products ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()
    

    