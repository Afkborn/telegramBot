
from posixpath import split
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, Updater, CallbackQueryHandler

from python.global_variables import SUPPORTED_DOMAIN
from .py_time import *
from python.Model.User import User
from python.Model.Product  import Product
from python.database import Database
from python.py_time import *
import time
import logging 
from playwright.sync_api import sync_playwright

myDb = Database()



def printLog(update: Update, functionName: str):
    logging.info(f"UID: {update.message.from_user.id} | command: {functionName}")
    print(f" {get_time_command()} UID: {update.message.from_user.id} | command: {functionName}")
    

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if myDb.getUserWithTelegramID(update.message.from_user.id) == None:
        user = User(telegram_id=update.message.from_user.id, is_bot=update.message.from_user.is_bot, username=update.message.from_user.username, first_name=update.message.from_user.first_name, last_name=update.message.from_user.last_name, language_code=update.message.from_user.language_code, created_at=time.time())
        myDb.addUser(user)
        logging.info(f"UID: {update.message.from_user.id} | created user, name: {user.get_username()}.")
        print(f" {get_time_command()} UID: {update.message.from_user.id} | created user, name: {user.get_username()}.")
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {update.message.from_user.first_name}, i'm a bot, maybe you can talk to me!\nFor more information, type /help"
    )
    
async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"track -> TEXT\nmyproducts -> TEXT\n "
    )



async def callback_handler(update : Update, context : CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    process , *_ = query.data.split(",")
    
    if process == "track":
        _, type, urlID, ownerID = query.data.split(",")
        #delete previous message
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        productLink = myDb.getUrlIndex(urlID)
        if (type =="stock"):
            productStokTakip = True
            productFiyatTakip = False
        elif (type =="price"):
            productStokTakip = False
            productFiyatTakip = True
        else:
            productStokTakip = True
            productFiyatTakip = True 
        
        productIsim = "TODO" #TODO İSİM AYARLA
        
        myProduct = Product(owner_telegram_id=int(ownerID), isim=productIsim, link=productLink, fiyat_takip=productFiyatTakip, stok_takip=productStokTakip, created_at=time.time(), fiyat=0,stok=0,son_kontrol_zamani=0)
        logging.info(f"{ownerID} | created product.")
        if myProduct.get_domain() in SUPPORTED_DOMAIN:
            myDb.addProduct(myProduct)
            logging.info(f"{ownerID} | added product to database")
            print(f" {get_time_command()} UID: {ownerID} | added product.")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You are now following this product, you will be notified when it changes.\nYou can check your products with /myproducts")
        else:
            print(f" {get_time_command()} UID: {ownerID} | product domain is not supported, domain: {myProduct.get_domain()}")
            logging.info(f"{ownerID} | product domain is not supported, domain: {myProduct.get_domain()}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="This domain is not supported, please try another one.")
            
    elif process == "myproducts":
        #delete previous message
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        _, type, productID, ownerID = query.data.split(",")
        myProduct = myDb.getProductWithProductID(productID)
        buttons = [
            [InlineKeyboardButton(text="Untrack", callback_data = f"untrack,{productID},{ownerID}")],
            [InlineKeyboardButton(text="Open", url =f"{myProduct.get_link()}")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Product Name: {myProduct.get_isim()}\nPrice: {myProduct.get_fiyat()}, Stock: {myProduct.get_stok_string()}, Tracking type: {myProduct.get_type()}", reply_markup = keyboard)
        
    elif process == "untrack":
        #delete previous message
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        _, productID, ownerID = query.data.split(",")
        if (myDb.deleteProductWithID(productID)):
            print(f" {get_time_command()} UID: {ownerID} | deleted product, productID:{productID}")
            logging.info(f"{ownerID} |deleted product, productID: {productID}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You are no longer following this product, you will not be notified when it changes.\nYou can check your products with /myproducts")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error")
    
    else:
        print(process)


async def myproducts(update: Update, context: CallbackContext.DEFAULT_TYPE):
    printLog(update, "myproducts")
    user = myDb.getUserWithTelegramID(update.message.from_user.id)
    if  user == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Please, type /start")
    else:
        products = myDb.getProductWithUser(user)
        buttons = []
        for product in products:
            if (product.get_fiyat_takip() and product.get_stok_takip()):
                type = "all"
            elif (product.get_fiyat_takip()):
                type = "price"
            else:
                type = "stock"
                
            buttons.append(
                [InlineKeyboardButton(text=product.get_isim(), callback_data = f"myproducts,{type},{product.get_id()},{update.message.from_user.id}")]
            )
        keyboard = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a product to track", reply_markup = keyboard)
        

async def track(update: Update, context: CallbackContext.DEFAULT_TYPE):
    printLog(update, "track")
    user = myDb.getUserWithTelegramID(update.message.from_user.id)
    if  user == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Please, type /start")
    else:
        url = (update.message.text).replace("/track ","")
        if (len(url) <= 6) or not ( url.startswith("http://") or url.startswith("https://")):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide URL")    
        else:
            
            #get product name
            
            
            urlIndex = myDb.addUrl(url)
            buttons = [
                    [InlineKeyboardButton(text = "Stock", callback_data = f"track,stock,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Price", callback_data = f"track,price,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Stock and Price", callback_data = f"track,all,{urlIndex},{update.message.from_user.id}")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(chat_id= update.effective_chat.id,text = 'What would you like to follow?', reply_markup = keyboard)
                                

async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f" {get_time_command()} - ID:{update.message.from_user.id} | {update.message.text}")    
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f" {get_time_command()} - ID:{update.message.from_user.id} | COMMAND ERROR {update.message.text}")
    logging.error(f"COMMAND ERROR | ID:{update.message.from_user.id} | {update.message.text}")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

