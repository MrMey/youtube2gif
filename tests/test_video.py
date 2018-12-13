import video
import os
import sys

def test_download():
    url = "https://www.youtube.com/watch?v=wYSmOVX1KJM"
    response = video.dl_youtube_url(url, 'output/video', True)
    print(response.keys())
    print('output/video/{}.{}'.format(response['id'],response['ext']))

def test_video_info():
    video_path = os.listdir('output/video')[0]
    duration, nb_frames = video.get_video_info('output/video/' + video_path)

def test_frame_to_gif():
    frames_path = 'output/frames'
    video.frames_to_gif(frames_path,'output/gif/mygif.gif',5)

def test_video_to_frames():
    duration, nb_frames = video.get_video_info("output/video/wYSmOVX1KJM.mp4")
    fps = nb_frames / float(duration)
    ratio = 3
    video.video_to_frames("output/video/wYSmOVX1KJM.mp4", "output/frames", 10, '00:00:10','00:00:20')

def test_optimize():
    video.optimize('output/gif/mygif.gif', 'output/gif/mygif2.gif')

def test_clear_output_folder():
    video.clear_output_folder('output')

if __name__ == "__main__":
    func = sys.argv[1]
    dic = {
        "test_download":test_download,
        "test_video_info":test_video_info,
        "test_frame_to_gif":test_frame_to_gif,
        "test_video_to_frames":test_video_to_frames,
        "test_clear_output_folder":test_clear_output_folder
    }
    dic[func]()