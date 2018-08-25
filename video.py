import os
import subprocess
import shutil
import youtube_dl


def init_output_folder(output_folder):
    if os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)


def async_dl_youtube_url(bot, job):
    print("start download")
    dl_youtube_url(job.context[0], job.context[1], job.context[2])
    print("finish download")

def dl_youtube_url(url, download, output_folder):
    ydl = youtube_dl.YoutubeDL({'outtmpl': output_folder + '/%(id)s'})

    with ydl:
        result = ydl.extract_info(
            url,
            download=download  # We just want to extract the info
        )
    return result


def video_to_frames(video_path, fps, output_folder, start=None, stop=None):

    command = 'ffmpeg  -i {} '.format(video_path)
    if start is not None:
        command += '-ss {} '.format(start)

    if stop is not None:
        command += '-to {} '.format(stop)

    command += '-r {} -vf scale=320:-1 "{}/frame-%03d.jpg"'.format(
        fps, output_folder)
    print(command)
    return os.system(command)


def get_video_info(video_path):
    command = "ffprobe -select_streams v -show_streams {} 2>/dev/null | grep -w duration".format(
        video_path)
    print(command)
    duration = str(subprocess.check_output(command, shell=True))
    duration = duration[:-3]
    duration = float(duration.rstrip('\n').split('=')[1])

    command = "ffprobe -select_streams v -show_streams {} 2>/dev/null | grep -w nb_frames".format(
        video_path)
    print(command)
    nb_frames = str(subprocess.check_output(command, shell=True))
    nb_frames = nb_frames[:-3]
    nb_frames = float(nb_frames.rstrip('\n').split('=')[1])
    print(nb_frames)
    return duration, nb_frames


def frames_to_gif(gif_path, output_folder, delay):
    command = "convert -delay {} -fuzz 2% -loop 0 {}/*.jpg {}".format(
        delay, output_folder, gif_path)
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
