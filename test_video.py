import video
import os


def test_download():
    url = "https://www.youtube.com/watch?v=SgzXKCuM9CA"
    response = video.dl_youtube_url(url, 'output/video')
    print(response.keys())
    print('output/video/{}.{}'.format(response['id'],response['ext']))

def test_video_info():
    video_path = os.listdir('output/video')[0]
    duration, nb_frames = video.get_video_info('output/video/' + video_path)

def test_frame_to_gif():
    frames_path = 'output/frames'
    video.frames_to_gif(frames_path,'output/gif/mygif.gif',5)

def test_video_to_frames():
    duration, nb_frames = video.get_video_info("output/video/SgzXKCuM9CA.mp4")
    fps = nb_frames / float(duration)
    ratio = 3
    video.video_to_frames("output/video/SgzXKCuM9CA.mp4", "output/frames", 10, '00:03:58.500','00:04:00.500')

def test_optimize():
    video.optimize('output/gif/mygif.gif', 'output/gif/mygif2.gif')

def test_clear_output_folder():
    video.clear_output_folder('output')

test_download()
#test_video_info()
#test_video_to_frames()
#test_frame_to_gif()
#test_optimize()
#test_clear_output_folder()