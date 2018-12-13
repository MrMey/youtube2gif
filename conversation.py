from functools import wraps
import os
import re
import time
import logging

import video

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
    logging.info('start')
    video.init_output_folder('output')
    bot.send_message(chat_id=update.message.chat_id,
                     text="Send me a youtube link to start")
    return 0


@restricted
def set_url(bot, update, user_data, job_queue):
    logging.info("set_url")

    url = update.message.text
    
    if url[:23] != "https://www.youtube.com":
        logging.warning("invalid url")
        bot.send_message(chat_id=update.message.chat_id,
                    text="please enter a secure youtube url like (https://www.youtube.com...)")
        return 0
    

    result = video.dl_youtube_url(url, False, 'output')
    user_data['id'] = result['id']
    user_data['ext'] = result['ext']

    bot.send_message(chat_id=update.message.chat_id,
                     text="video is downloading")

    dl_job = job_queue.run_once(video.async_dl_youtube_url, when=10,context=[url, True, 'output'])
    print(dl_job)
    print(job_queue._queue)

    iter = True
    count = 0
    while iter:
        if os.path.isfile('output/' + user_data['id'] + '.' + user_data['ext']):
            iter = False
        if os.path.isfile('output/' + user_data['id'] + '.mkv'):
            iter = False
        if count > 1000:
            iter = False
        time.sleep(10)


    bot.send_message(chat_id=update.message.chat_id,
                     text="start time? (%H:%M:%S.xxx)")

    return 1

@restricted
def set_start_time(bot, update, user_data):
    logging.info("set_start_time")

    start = update.message.text

    if start == "":
        start = "00:00:00"

    if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", start):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", start):
            bot.send_message(chat_id=update.message.chat_id,
                        text="wrong time format (%H:%M:%S.xxx)")
            return 1

    user_data['start'] = start

    bot.send_message(chat_id=update.message.chat_id,
                    text="stop time? (%H:%M:%S.xxx)")
    
    return 2

@restricted
def set_stop_time(bot, update, user_data):
    logging.info("set_stop_time")

    stop = update.message.text

    if stop == "":
        stop = "00:00:00"

    if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$", stop):
        if not re.match(r"^(2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])\.([0-9]{0,3})$", stop):
            bot.send_message(chat_id=update.message.chat_id,
                        text="wrong time format (%H:%M:%S.xxx)")
            return 2

    user_data['stop'] = stop

    bot.send_message(chat_id=update.message.chat_id,
                text="starting the magic !")

    video_path = 'output/' + user_data['id'] +'.'
    if os.path.isfile(video_path + user_data['ext']):
        video_path += user_data['ext']
    elif os.path.isfile(video_path + 'mkv'):
        video_path += 'mkv'
    else:
        logging.error('video file not found')
        return 0
    
    video.video_to_frames(video_path, 10,'output', user_data['start'], user_data['stop'])
    video.frames_to_gif('output/{}.gif'.format(user_data['id']),'output', 5)

    bot.send_message(chat_id=update.message.chat_id,
                     text="gif saved")
    
    gif_path = 'output/' + user_data['id'] + '.gif'
    print(gif_path)
    bot.send_video(chat_id=update.message.chat_id,
                    video=open(gif_path,'rb'))

    # TODO clear folder
    return 0
