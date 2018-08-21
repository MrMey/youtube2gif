# coding: utf8

from functools import wraps
import os
import datetime
import re
import json
import logging
import logging.config
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.ext import Updater, CommandHandler, Filters
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler

import video

# If applicable, delete the existing log file to generate a fresh log file during each execution
if os.path.isfile("run_log.log"):
    os.remove("run_log.log")

with open("log_config.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)
 
logging.config.dictConfig(config_dict)
 
# Log that the logger was configured
logger = logging.getLogger(__name__)

ZERO, ONE, TWO = range(3)


token = "605391156:AAE2q2zhFjmysZcMoDgXyg8UxmfsKaLaOhc" #os.environ.get("TELEGRAM_TOKEN")
# list of authorized id
auth_ids = [171531269]

# decorator to restrict access to the bot
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in auth_ids:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


@restricted
def start(bot, update):
    logger.info('start')
    bot.send_message(chat_id=update.message.chat_id,
                     text="Send me a youtube link to start")
    return ZERO


@restricted
def set_url(bot, update, user_data):
    logger.info("set_url")

    url = update.message.text
    
    if url[:23] != "https://www.youtube.com":
        logger.warning("invalid url")
        bot.send_message(chat_id=update.message.chat_id,
                    text="please enter a secure youtube url like (https://www.youtube.com...)")
        return ZERO
    
    result = video.dl_youtube_url(url,'output/video')
    user_data['id'] = result['id']
    user_data['ext'] = result['ext']

    bot.send_message(chat_id=update.message.chat_id,
                     text="video saved")

    bot.send_message(chat_id=update.message.chat_id,
                     text="start time? (%H:%M:%S.xxx)")

    return ONE


def set_start_time(bot, update, user_data):
    logger.info("set_start_time")

    start = update.message.text

    if start == "":
        start = "00:00:00"

    if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", start):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", start):
            bot.send_message(chat_id=update.message.chat_id,
                        text="wrong time format (%H:%M:%S.xxx)")
            return ONE

    user_data['start'] = start

    bot.send_message(chat_id=update.message.chat_id,
                    text="stop time? (%H:%M:%S.xxx)")
    
    return TWO

def set_stop_time(bot, update, user_data):
    logger.info("set_stop_time")

    stop = update.message.text

    if stop == "":
        stop = "00:00:00"

    if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", stop):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", stop):
            bot.send_message(chat_id=update.message.chat_id,
                        text="wrong time format (%H:%M:%S.xxx)")
            return TWO

    user_data['stop'] = stop

    bot.send_message(chat_id=update.message.chat_id,
                text="starting the magic !")

    video_path = 'output/video/' + user_data['id'] + '.mkv'
    video.video_to_frames(video_path,'output/frames', 10, user_data['start'], user_data['stop'])
    video.frames_to_gif('output/frames','output/gif/{}.gif'.format(user_data['id']), 5)

    bot.send_message(chat_id=update.message.chat_id,
                     text="gif saved")
    
    gif_path = 'output/gif/' + user_data['id'] + '.gif'
    bot.send_video(chat_id=update.message.chat_id,
                    video=open(gif_path,'rb'))
    video.clear_output_folder('output')
    return ZERO

updater = Updater(token)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ZERO: [MessageHandler(Filters.text, set_url, pass_user_data=True)],
        ONE: [MessageHandler(Filters.text, set_start_time, pass_user_data=True)],
        TWO: [MessageHandler(Filters.text, set_stop_time, pass_user_data=True)]        
    },
    fallbacks=[CommandHandler('start', start)]
)

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
