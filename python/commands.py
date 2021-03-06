
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from python.global_variables import AVAIBLE_COMMANDS, SUPPORTED_DOMAIN
from .py_time import *
from python.Model.User import User
from python.Model.Product  import Product
from python.database import Database
from python.py_time import *

from python.token import *
import time
import logging 

myDb = Database()



def printLog(update: Update, functionName: str):
    logging.info(f"UID: {update.message.from_user.id} | command: {functionName}")
    print(f" {get_time_command()} UID: {update.message.from_user.id} | command: {functionName}")
    

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    
    
    
    if myDb.getUserWithTelegramID(update.message.from_user.id) == None:
        user = User(telegram_id=update.message.from_user.id,
                    is_bot=update.message.from_user.is_bot,
                    username=update.message.from_user.username,
                    first_name=update.message.from_user.first_name,
                    last_name=update.message.from_user.last_name,
                    language_code=update.message.from_user.language_code,
                    created_at=time.time()
                    )
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
    process , *_ = query.data.split(",") # TRACK
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
        
        productIsim = "TODO"
        myProduct = Product(owner_telegram_id=int(ownerID),
                            isim=productIsim,
                            link=productLink,
                            fiyat_takip=productFiyatTakip,
                            stok_takip=productStokTakip,
                            created_at=time.time(),
                            fiyat=0,
                            stok=0,
                            son_kontrol_zamani=0,
                            birim_id=1,
                            )
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
            [InlineKeyboardButton(text="Open", url =f"{myProduct.get_link()}")],
            [InlineKeyboardButton(text="Close", callback_data = f"closeProduct")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        if (myProduct.get_isim() == "TODO"):
            isim = "Getting name, please wait..."
        else:
            isim = myProduct.get_isim()
        if (myProduct.get_birim_id() == 1):
            birim = ""
        else:
            birim = myDb.getSimgeFromID(myProduct.get_birim_id())
    
        if (myProduct.get_fiyat_takip() and myProduct.get_stok_takip()):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Product Name: {isim}\nPrice: {myProduct.get_fiyat()} {birim}, Stock: {myProduct.get_stok_string()}", reply_markup = keyboard)
        elif (myProduct.get_fiyat_takip()):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Product Name: {isim}\nPrice: {myProduct.get_fiyat()} {birim}", reply_markup = keyboard)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Product Name: {isim}\nStock: {myProduct.get_stok_string()}", reply_markup = keyboard)
        
        
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
            
    elif process == "closeProduct":
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        
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
        if (len(products) == 0):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not following any product. Please, type /track")
        else:
            for product in products:
                if (product.get_fiyat_takip() and product.get_stok_takip()):
                    type = "all"
                elif (product.get_fiyat_takip()):
                    type = "price"
                else:
                    type = "stock"
                    
                if (product.get_isim() == "TODO"):
                    isim = "Getting name, please wait..."
                else:
                    isim = product.get_isim()
                    
                buttons.append(
                    [InlineKeyboardButton(text=isim, callback_data = f"myproducts,{type},{product.get_id()},{update.message.from_user.id}")]
                )
                
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a product to track", reply_markup = keyboard)
        

async def track(update: Update, context: CallbackContext.DEFAULT_TYPE):
    printLog(update, "track")
    
    user = myDb.getUserWithTelegramID(update.message.from_user.id)
    if  user == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Please, type /start")
    else:
        url = (update.message.text).replace("/track ","") # just URL
        if (len(url) <= 6) or not ( url.startswith("http://") or url.startswith("https://")):  # check if URL is valid
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide URL")    
        else:
            #https://www.amazon.com.tr/manyetik-Phillips-Security-Pentalobe-Tri-Point/dp/B0189YWOIO/?_encoding=UTF8&pd_rd_w=ua3MV&pf_rd_p=a05c0273-b826-4efe-ba61-63c1fc2e261a&pf_rd_r=S6RTZY937SPQQJSRQPCQ&pd_rd_r=94a32f9f-95d3-4f7b-8872-0a43cf72d8ce&pd_rd_wg=zrJe8&ref_=pd_gw_cr_wsim
            # 1
            urlIndex = myDb.addUrl(url) 
            buttons = [
                    [InlineKeyboardButton(text = "Stock", callback_data = f"track,stock,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Price", callback_data = f"track,price,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Stock and Price", callback_data = f"track,all,{urlIndex},{update.message.from_user.id}")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(chat_id= update.effective_chat.id,text = 'What would you like to follow?', reply_markup = keyboard)
                                

async def echoMessage(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f" {get_time_command()} - ID:{update.message.from_user.id} | {update.message.text}")    
    isAvaible = False
    slashCheck = False
    for commands in AVAIBLE_COMMANDS:
        if not commands in update.message.text:
            isAvaible = True
        elif commands  == update.message.text:
            slashCheck = True
            await context.bot.send_message(chat_id=update.effective_chat.id, text="'/' yazmay?? unutmu?? olabilir misin? ????")      
    if (isAvaible and not slashCheck):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="B??yle bir komut bulunamad??.")      
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def unknownCommand(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f" {get_time_command()} - ID:{update.message.from_user.id} | COMMAND ERROR {update.message.text}")
    logging.error(f"COMMAND ERROR | ID:{update.message.from_user.id} | {update.message.text}")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

