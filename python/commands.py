
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, Updater, CallbackQueryHandler
from .py_time import *
from python.Model.User import User
from python.Model.Product  import Product
from python.database import Database
import time
import logging 

myDb = Database()


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if myDb.getUserWithTelegramID(update.message.from_user.id) == None:
        user = User(telegram_id=update.message.from_user.id, is_bot=update.message.from_user.is_bot, username=update.message.from_user.username, first_name=update.message.from_user.first_name, last_name=update.message.from_user.last_name, language_code=update.message.from_user.language_code, created_at=time.time())
        myDb.addUser(user)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {update.message.from_user.first_name}, i'm a bot, maybe you can talk to me!\nFor more information, type /help"
    )
    
async def help(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"HELP TEXT"
    )


async def callback_handler(update : Update, context : CallbackContext.DEFAULT_TYPE):
    query = update.callback_query
    process, type, urlID, ownerID = query.data.split(",")
    if process == "track":
        #delete previous message
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        logging.info("delete previous message")
        
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
        productIsim = "TODO" #TODO ISIM UNUTMA
        myProduct = Product(owner_telegram_id=int(ownerID), isim=productIsim, link=productLink, fiyat_takip=productFiyatTakip, stok_takip=productStokTakip, created_at=time.time(), fiyat=0,stok=0,son_kontrol_zamani=0)
        logging.info("created product")
        print(myProduct)
        myDb.addProduct(myProduct)
        logging.info("added product")

async def track(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = myDb.getUserWithTelegramID(update.message.from_user.id)
    if  user == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Please, type /start")
    else:
        url = (update.message.text).replace("/track ","")
        print(len(url))
        if (len(url) <= 6) or not ( url.startswith("http://") or url.startswith("https://")):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide URL")    
        else:
            urlIndex = myDb.addUrl(url)
            buttons = [
                    [InlineKeyboardButton(text = "Stock", callback_data = f"track,stock,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Price", callback_data = f"track,price,{urlIndex},{update.message.from_user.id}")],
                    [InlineKeyboardButton(text = "Stock and Price", callback_data = f"track,all,{urlIndex},{update.message.from_user.id}")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(chat_id= update.effective_chat.id,text = 'What would you like to follow?', reply_markup = keyboard)
                                
        
async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f"{get_time_command()} - ID:{update.message.from_user.id} | {update.message.text}")
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f"{get_time_command()} - ID:{update.message.from_user.id} | COMMAND ERROR {update.message.text}")
    logging.error(f"COMMAND ERROR | ID:{update.message.from_user.id} | {update.message.text}")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

