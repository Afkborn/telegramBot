
from python.compatibility import *
from python.py_logging import *
from python.global_variables import *
from python.py_time import * 
from python import commands as cmd

import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, CallbackQueryHandler




if __name__  == "__main__":
    setLogging()
    if (checkCompatibility()):
        
        
        print(f"{get_time_command()} | Compatibility check passed.")
        logging.info("Compatibility is OK")
        
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        logging.info("Application is built")
        print(f"{get_time_command()} | Application is built.")
        
        start_handler = CommandHandler('start', cmd.start) # /start
        application.add_handler(start_handler)
        logging.info("Add start handler")

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), cmd.echo)
        application.add_handler(echo_handler)
        logging.info("Add echo handler")
        
        help_handler = CommandHandler('help', cmd.help) # /help
        application.add_handler(help_handler)
        logging.info("Add help handler")
        
        application.add_handler(CallbackQueryHandler(cmd.callback_handler))  # callback
        logging.info("Add callback handler")
        
        track_handler = CommandHandler('track', cmd.track) # /track
        application.add_handler(track_handler)
        logging.info("Add track handler")
        
        
        myproducts_handler = CommandHandler('myproducts', cmd.myproducts) # /myproducts
        application.add_handler(myproducts_handler)
        logging.info("Add myproducts handler")
        

        
        unknown_handler = MessageHandler(filters.COMMAND, cmd.unknown)
        application.add_handler(unknown_handler)
        logging.info("Add unknown handler")
        

        
        logging.info("Start polling")
        print(f"{get_time_command()} | Running...")
        
        application.run_polling(stop_signals=None)

        
        