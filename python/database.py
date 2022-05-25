import sqlite3 as sql
from time import time 

from python.Model.User import User
from python.Model.Product import Product
from python.global_variables import *



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
        self.im.execute(CREATETABLE_PRICES)
        self.im.execute(CREATETABLE_BIRIM)
        self.checkDefaultBirim()
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
    
    def checkDefaultBirim(self):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM birimler WHERE id = 1")
        result = self.im.fetchone()
        if result == None:
            self.addDefaultBirim()
        return True
    
    def getBirimFromSimge(self, simge:str) -> str:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM birimler WHERE simge = '{simge}'")
        result = self.im.fetchone()
        if result == None:
            return None
        id,birim,simge = result
        self.db.close()
        return id,birim,simge
    
    def getSimgeFromID(self, id : int) -> str:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM birimler WHERE id = {id}")
        result = self.im.fetchone()
        if result == None:
            return None
        _ ,_, simge = result
        self.db.close()
        return simge
    
    def addDefaultBirim(self):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"birim,simge"
        VALUES = f"""
        ' ',
        ' '
        """
        self.im.execute(f"INSERT INTO birimler ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()    
    
    def addBirim(self, birim:str, simge:str):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"birim,simge"
        VALUES = f"""
        '{birim}',
        '{simge}'
        """
        self.im.execute(f"INSERT INTO birimler ({KEY}) VALUES ({VALUES})")
        last_insert_rowid = self.im.lastrowid
        self.db.commit()
        self.db.close()
        return last_insert_rowid
    
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
        KEY = f"owner_telegram_id,isim,link,fiyat_takip,stok_takip,fiyat,stok,son_kontrol_zamani,created_at,birim_id"
        VALUES = f"""
        '{product.get_owner_telegram_id()}',
        '{product.get_isim()}',
        '{product.get_link()}',
        '{product.get_fiyat_takip()}',
        '{product.get_stok_takip()}',
        '{product.get_fiyat()}',
        '{product.get_stok()}',
        '{product.get_son_kontrol_zamani()}',
        '{product.get_created_at()}',
        '{product.get_birim_id()}'
        """
        self.im.execute(f"INSERT INTO products ({KEY}) VALUES ({VALUES})")
        last_row_index = self.im.lastrowid
        product.set_id(last_row_index)
        self.db.commit()
        self.db.close()
        self.addPrice(product)
        return product 
    
    def addPrice(self, product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        KEY = f"product_id,fiyat,time"
        VALUES = f"""
        '{product.get_id()}',
        '{product.get_fiyat()}',
        '{time()}'
        """    
        self.im.execute(f"INSERT INTO prices ({KEY}) VALUES ({VALUES})")
        self.db.commit()
        self.db.close()
    
    def updateProductPrice(self, product:Product, price : float):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE products SET fiyat = '{price}' WHERE id = '{product.get_id()}'")
        self.db.commit()
        self.db.close()
        self.addPrice(product,price)
        
    def getProductWithUser(self, user : User) -> list[Product]:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM products WHERE owner_telegram_id = '{user.get_telegram_id()}'")
        results = self.im.fetchall()
        productList = []
        for result in results:
            id, owner_telegram_id, isim, link, fiyat_takip, stok_takip, fiyat, stok, son_kontrol_zamani, created_at, birim_id = result
            myResult = Product(id=id,owner_telegram_id=owner_telegram_id,isim=isim,link=link,fiyat_takip=fiyat_takip,stok_takip=stok_takip,fiyat=fiyat,stok=stok,son_kontrol_zamani=son_kontrol_zamani,created_at=created_at,birim_id=birim_id)
            productList.append(myResult)
        self.im.close()
        self.db.close()
        return productList   
    
    def getProductWithProductID(self, ID:int ) -> Product:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM products WHERE id = '{ID}'")
        result = self.im.fetchone()
        id, owner_telegram_id, isim, link, fiyat_takip, stok_takip, fiyat, stok, son_kontrol_zamani, created_at, birim_id = result
        myProduct = Product(id=id,owner_telegram_id=owner_telegram_id,isim=isim,link=link,fiyat_takip=fiyat_takip,stok_takip=stok_takip,fiyat=fiyat,stok=stok,son_kontrol_zamani=son_kontrol_zamani,created_at=created_at,birim_id=birim_id)
        self.im.close()
        self.db.close()
        return myProduct
    
    def deleteProductWithID(self, ID:int) -> bool:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"DELETE FROM products WHERE id = '{ID}'")
        self.db.commit()
        self.im.close()
        self.db.close()
        return True

    def getAllProduct(self) -> list[Product]:
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM products")
        results = self.im.fetchall()
        productList = []
        for result in results:
            id, owner_telegram_id, isim, link, fiyat_takip, stok_takip, fiyat, stok, son_kontrol_zamani, created_at, birim_id = result
            myResult = Product(id=id,owner_telegram_id=owner_telegram_id,isim=isim,link=link,fiyat_takip=fiyat_takip,stok_takip=stok_takip,fiyat=fiyat,stok=stok,son_kontrol_zamani=son_kontrol_zamani,created_at=created_at,birim_id=birim_id)
            productList.append(myResult)
        self.im.close()
        self.db.close()
        return productList    
    
    def updatePriceAndStokFromProduct(self, product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE products SET fiyat = '{product.get_fiyat()}', stok = '{product.get_stok()}' WHERE id = '{product.get_id()}'")
        self.db.commit()
        self.im.close()
        self.db.close()
        
    def updateSonKontrolZamaniProduct(self,product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE products SET son_kontrol_zamani = '{product.get_son_kontrol_zamani()}' WHERE id = '{product.get_id()}'")
        self.db.commit()
        self.im.close()
        self.db.close()
        
    def updateIsimProduct(self,product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE products SET isim = '{product.get_isim()}' WHERE id = '{product.get_id()}'")
        self.db.commit()
        self.im.close()
        self.db.close()
        
    def updateBirimIDProduct(self,product:Product):
        self.db = sql.connect(self.dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE products SET birim_id = '{product.get_birim_id()}' WHERE id = '{product.get_id()}'")
        self.db.commit()
        self.im.close()
        self.db.close()

    