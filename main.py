# coding: utf8

import os
import json
import logging
import logging.config

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.ext import Updater, CommandHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler

from conversation import start, set_start_time, set_stop_time, set_url
import video

# If applicable, delete the existing log file to generate a fresh log file during each execution
if os.path.isfile("run_log.log"):
    os.remove("run_log.log")

with open("log_config.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)
 
logging.config.dictConfig(config_dict)
 
# Log that the logger was configured
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if TOKEN is None:
    with open("bot_config.json","r") as bot_configuration_file:
        bot_config_dict = json.load(bot_configuration_file)
    TOKEN = bot_config_dict["token"]
    WEBHOOK = False
else:
    WEBHOOK = True

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
# add handlers
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        0: [MessageHandler(Filters.text, set_url, pass_user_data=True)],
        1: [MessageHandler(Filters.text, set_start_time, pass_user_data=True)],
        2: [MessageHandler(Filters.text, set_stop_time, pass_user_data=True, pass_job_queue=True)]
        
    },
    fallbacks=[CommandHandler('start', start)]
)

updater.dispatcher.add_handler(conv_handler)

video.init_output_folder("output")

if WEBHOOK:
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://agile-springs-16890.herokuapp.com/" + TOKEN)
    updater.idle()
else:
    updater.start_polling()