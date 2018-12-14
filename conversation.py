from functools import wraps
import os
import re
import time
import logging

import video
import gif

# list of authorized id
auth_ids = [171531269, 571432478]

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
    logging.info('start')
    bot.send_message(chat_id=update.message.chat_id,
                     text="Send me a youtube link to start")
    return 0


@restricted
def set_url(bot, update, user_data):
    logging.info("set_url")

    video.clear_user_files('output', str(update.effective_user.id))
    url = update.message.text
    user_data["gif"] = gif.Gif(str(update.effective_user.id))

    try:
        user_data["gif"].url = url
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="please enter a secure youtube url like (https://www.youtube.com...)")
        return 0

    output_path = "output/" + str(update.effective_user.id)
    user_data["gif"].set_metadata(
        video.dl_youtube_url(url, False, output_path))

    bot.send_message(chat_id=update.message.chat_id,
                     text="start time? (%H:%M:%S.xxx)")

    return 1


@restricted
def set_start_time(bot, update, user_data):
    logging.info("set_start_time")

    start = update.message.text

    try:
        user_data["gif"].set_start_time(start)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="wrong time format (%H:%M:%S.xxx)")
        return 1

    bot.send_message(chat_id=update.message.chat_id,
                     text="stop time? (%H:%M:%S.xxx)")

    return 2


@restricted
def set_stop_time(bot, update, user_data, job_queue):
    logging.info("set_stop_time")

    stop = update.message.text

    try:
        user_data["gif"].set_stop_time(stop)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="wrong time format (%H:%M:%S.xxx) or stop time before start time")
        return 2

    bot.send_message(chat_id=update.message.chat_id,
                     text="starting the magic !")

    logging.info("start download")

    video.dl_youtube_url(user_data["gif"].url, True, 'output/'+user_data["gif"].id)
    logging.info("finish download")

    video_path = "output/" + user_data["gif"].id + '.'
    print(video_path)
    if os.path.isfile(video_path + user_data["gif"].metadata["ext"]):
        video_path += user_data["gif"].metadata["ext"]
    elif os.path.isfile(video_path + 'mkv'):
        video_path += 'mkv'
    else:
        logging.error('video file not found')
        return 0
    
    video.video_to_frames(video_path, 10,
                          'output',
                          user_data["gif"].id,
                          user_data["gif"].start_time,
                          user_data["gif"].stop_time)

    video.frames_to_gif('output/{}.gif'.format(user_data["gif"].id),
                        'output',
                        user_data["gif"].id,
                        5)

    gif_path = 'output/' + user_data["gif"].id + '.gif'
    print(gif_path)
    bot.send_video(chat_id=update.message.chat_id,
                   video=open(gif_path, 'rb'))

    bot.send_message(chat_id=update.message.chat_id,
                   text="Send me a youtube link to start")
    return 0

