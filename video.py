import os
import subprocess
import shutil
import youtube_dl


def clear_output_folder(output_folder):
    shutil.rmtree(output_folder + '/video')
    os.mkdir(output_folder + '/video')
    shutil.rmtree(output_folder + '/frames')
    os.mkdir(output_folder + '/frames')
    shutil.rmtree(output_folder + '/gif')
    os.mkdir(output_folder + '/gif')


def async_dl_youtube_url(bot, job):
    dl_youtube_url(job.context[0], job.context[1])


def dl_youtube_url(url, output_folder):
    ydl = youtube_dl.YoutubeDL({'outtmpl': output_folder + '/video'})

    with ydl:
        result = ydl.extract_info(
            url,
            download=True  # We just want to extract the info
        )
    return result


def get_output_file_path(output_folder, fmt=[]):
    file_name = os.listdir(output_folder)

    if len(file_name) == 0:
        raise Exception('no video file found')
    if len(file_name) > 1:
        raise Exception('flush file before running')

    file_name = file_name[0]
    if file_name.split('.')[-1] not in fmt:
        raise Exception('wrong format for file')
    return output_folder + '/' + file_name


def video_to_frames(video_path, output_folder, fps, start=None, stop=None):

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


def frames_to_gif(frames_folder, gif_path, delay):
    command = "convert -delay {} -fuzz 2% -loop 0 {}/*.jpg {}".format(
        delay, frames_folder, gif_path)
    print(command)
    response = os.system(command)

    return response


def select_frames(frame_folder, start, stop):
    frame_list = [frame_folder +
                  '/frame-{}.jpg'.format(x) for x in range(start, stop)]
    for file in frame_list:
        shutil.copy(file, 'output/sub_frames')


def optimize(input_path, output_path, mode='-O3'):
    command = 'gifsicle {}'.format(input_path)
    command += ' --colors 256 '
    command += mode
    command += ' > '
    command += '{}'.format(output_path)
    print(command)
    response = os.system(command)

    return response
