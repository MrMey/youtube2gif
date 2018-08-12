import os
import subprocess
import shutil


def clear_output_folder(output_folder):
    shutil.rmtree(output_folder + '/video')
    os.mkdir(output_folder + '/video')
    shutil.rmtree(output_folder + '/frames')
    os.mkdir(output_folder + '/frames')
    shutil.rmtree(output_folder + '/gif')
    os.mkdir(output_folder + '/gif')


def dl_youtube_url(url, output_folder):
    cwd = os.getcwd()
    os.chdir(output_folder)
    command = "youtube-dl -f mp4 -o '%(id)s.%(ext)s' '{}'".format(url)
    print(command)
    response = os.system(command)

    if response != 0:
        raise Exception('command failed')
    os.chdir(cwd)
    return response


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

    command += '-r {} -vf scale=320:-1 "{}/frame-%03d.jpg"'.format(fps, output_folder)
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