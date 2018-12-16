import os
import subprocess
import shutil
import youtube_dl
import logging

logger = logging.getLogger("main.video")


def clear_user_files(output_folder, user_id):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    list_file = os.listdir(output_folder)
    for file in list_file:
        if file.startswith(user_id):
            os.remove("output/"+file)


def init_output_folder(output_folder):
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)


def async_process(bot, job):
    logger.info("start download")
    gif = job.context[0]

    dl_youtube_url(gif.url, True, 'output/'+gif.id)
    logger.info("finish download")

    video_path = "output/" + gif.id + '.'
    print(video_path)
    if os.path.isfile(video_path + gif.metadata["ext"]):
        video_path += gif.metadata["ext"]
    elif os.path.isfile(video_path + 'mkv'):
        video_path += 'mkv'
    else:
        logger.error('video file not found')
        return 0

    video_to_frames(video_path, 10,
                    'output',
                    gif.id,
                    gif.start_time,
                    gif.stop_time)

    frames_to_gif('output/{}.gif'.format(gif.id),
                  'output',
                  gif.id,
                  5)

    gif_path = 'output/' + gif.id + '.gif'
    print(gif_path)
    bot.send_video(chat_id=job.context[1],
                   video=open(gif_path, 'rb'))
    return 0


def dl_youtube_url(url, download, output_path):
    ydl = youtube_dl.YoutubeDL({'outtmpl': output_path})

    with ydl:
        result = ydl.extract_info(
            url,
            download=download  # We just want to extract the info
        )
    return result


def extract_video(video_path, output_path, start, stop):
    command = 'ffmpeg -ss {} -i {} -to {} -vcodec copy -an {}'.format(start,
                                                                              video_path,
                                                                              stop,
                                                                              output_path)
    logger.info(command)
    return os.system(command)


def video_to_frames(video_path, fps, output_folder, user_id, start=None, stop=None):

    command = 'ffmpeg  -i {} '.format(video_path)
    if start is not None:
        command += '-ss {} '.format(start)

    if stop is not None:
        command += '-to {} '.format(stop)

    command += '-r {} -vf scale=320:-1 "{}/{}-%03d.jpg"'.format(
        fps, output_folder, user_id)
    print(command)
    return os.system(command)


def frames_to_gif(gif_path, output_folder, user_id, delay):
    command = "convert -delay {} -fuzz 2% -loop 0 {}/{}-*.jpg {}".format(
        delay, output_folder, user_id, gif_path)
    print(command)
    response = os.system(command)

    return response


def optimize(input_path, output_path, mode='-O3'):
    command = 'gifsicle {}'.format(input_path)
    command += ' --colors 256 '
    command += mode
    command += ' > '
    command += '{}'.format(output_path)
    print(command)
    response = os.system(command)

    return response
