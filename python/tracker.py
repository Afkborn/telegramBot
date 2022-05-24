
from python.Model.Product import Product
from python.database import Database
from python.global_variables import TELEGRAM_TOKEN

from python.py_time import *

import time

from python.commands import  *


import requests

from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

class Tracker():
    # Kontrol edilmesi gereken ürünleri bulur, onların kontrolünü sağlar
    
    productList : Product = list() # list of products
    productToFollow : Product = list() #list of products to check
    controlTime = 0 #in seconds # 
    
    lastTrackTime = 0.0
    
    controlSleepTime = 0 # in seconds
    
    def __init__(self) -> None:
        self.db = Database()

    def updateProductList(self):
        self.productList.clear()
        self.productList = self.db.getAllProduct()
    
    def getControlTime(self):
        # Her bir ürünün kaç saniyede bir kontrol edileceğini belirler
        self.controlTime = 600
        
    def getControlSleepTime(self):
        # Kontrol edilmesi gereken ürünleri bulurken bekleyeceği süre, buradaki amaç her saniye hangi ürünün kontrülünü yapılacağını görmenin gereksiz olacağından kaynaklı
        self.controlSleepTime = 60
          
    def getProductsToFollow(self):
        self.updateProductList()
        self.getControlTime()
        self.productToFollow.clear()
        for product in self.productList:
            product_time = product.get_son_kontrol_zamani()
            if time.time() > (product_time + self.controlTime):
                self.productToFollow.append(product)
        if (len(self.productToFollow) == 0):
            print(f" {get_time_command()} | Kontrol edilecek ürün yok.")
            logging.info(f" Kontrol edilecek ürün yok.")
        else:
            logging.info(f" Kontrol edilecek ürün sayısı: {len(self.productToFollow)}")
            print(f" {get_time_command()} | Takip zamanı geçen {len(self.productToFollow)} adet ürün var.")
        return self.productToFollow
    
    
    def sendMessage(self,userID : int, message : str):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={userID}&text={message}"
        requests.get(url)
    
    def clearFiyat(self,fiyat:str) -> int:
        fiyat = float(fiyat.replace("TL", "").replace(".", "").replace(",", "."))
        return fiyat
    

    
    def trackProduct(self, product : Product) -> None:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
    
            if (product.get_domain() == SUPPORTED_DOMAIN[0]): # amazon.com.tr
                self.getPriceAndStockFromAmazon(page, product)
            else:
                print("Bu ürünün kontrolü henüz desteklenmiyor.")
                self.sendMessage(product.get_owner_telegram_id(),f"{product.get_domain()} bu domain desteklenmiyor.")
            browser.close()
    
    def setTracker(self):
        self.getControlSleepTime()
        while True:
            if ((self.lastTrackTime + self.controlSleepTime) < time.time()):
                print(f" {get_time_command()} | Kontrol zamanı gelmiş, kontrol yapılıyor.")
                self.getProductsToFollow()
                for product in self.productToFollow:
                    self.trackProduct(product)
                self.lastTrackTime = time.time()
                time.sleep(self.controlSleepTime)
                
    def getPriceAndStockFromAmazon(self, page :Page, product : Product) -> None:
            page.goto(product.get_link()) # amazon.com.tr ürünün linkini açar
            corePrice_element = page.query_selector("div[id^='corePrice_']")
            fiyat = corePrice_element.query_selector('span[class="a-offscreen"]').inner_text()
            fiyat = self.clearFiyat(fiyat=fiyat)
            if (product.get_fiyat() != fiyat):
                product.set_fiyat(fiyat)
                product.set_son_kontrol_zamani(time.time())
                self.sendMessage(product.get_owner_telegram_id(), f"{product.get_isim()} ürününün fiyatı değişti.\nYeni Fiyat: {product.get_fiyat()}")
                print(f" {get_time_command()} | {product.get_isim()} ürününün fiyatı değişti.\nYeni Fiyat: {product.get_fiyat()}")
                myDb.addPrice(product)
                myDb.updatePriceAndSonKontrolZamaniFromProduct(product)
            else:
                print(f" {get_time_command()} | ID: {product.get_id()} {product.get_isim()} ürününün fiyatı değişmedi.")
                logging.info(f" ID: {product.get_id()} {product.get_isim()} ürününün fiyatı değişmedi.")