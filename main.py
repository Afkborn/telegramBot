
from python.compatibility import *
from python.py_logging import *
from python.global_variables import *

import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, filters, MessageHandler, CallbackQueryHandler


from python import commands as cmd

if __name__  == "__main__":
    setLogging()
    if (checkCompatibility()):
        logging.info("Compatibility is OK")
        
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        logging.info("Application is built")
        
        start_handler = CommandHandler('start', cmd.start) # /start
        application.add_handler(start_handler)

        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), cmd.echo)
        application.add_handler(echo_handler)
        
        
        help_handler = CommandHandler('help', cmd.help) # /help
        application.add_handler(help_handler)
        
        track_handler = CommandHandler('track', cmd.track) # /track
        application.add_handler(track_handler)
        
        
        application.add_handler(CallbackQueryHandler(cmd.callback_handler))  # callback
        
        
        unknown_handler = MessageHandler(filters.COMMAND, cmd.unknown)
        application.add_handler(unknown_handler)
         
        application.run_polling(stop_signals=None)

        
        