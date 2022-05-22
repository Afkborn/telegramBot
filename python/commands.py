
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, Updater, CallbackQueryHandler
from .py_time import *
from python.Model.User import User
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
    process, type, url = query.data.split(",")
    if process == "track":
        #delete previous message
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        print(url,type)
        
    

async def track(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = myDb.getUserWithTelegramID(update.message.from_user.id)
    if  user == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Please, type /start")
    else:
        url = (update.message.text).replace("/track ","")
        if (len(url) <= 6) or (url[:7] != "http://" and url[:8] != "https://" ):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You need to provide URL")    
        else:
            buttons = [
                [InlineKeyboardButton(text = "Stock", callback_data = f"track,stock,{url}")],
                [InlineKeyboardButton(text = "Price", callback_data = f"track,price,{url}")],
                [InlineKeyboardButton(text = "Stock and Price", callback_data = f"track,all,{url}")]
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            await context.bot.sendMessage(chat_id= update.effective_chat.id,text = 'What would you like to follow?', reply_markup = keyboard)
                                
        
async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f"{get_time_command()} - ID:{update.message.from_user.id} | {update.message.text}")
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print(f"{get_time_command()} - ID:{update.message.from_user.id} | COMMAND ERROR {update.message.text}")
    logging.error(f"COMMAND ERROR | ID:{update.message.from_user.id} | {update.message.text}")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

