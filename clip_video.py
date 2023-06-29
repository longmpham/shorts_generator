import random
import time
import os
from moviepy.editor import VideoFileClip

def create_random_subclips(mp4_file, subclip_duration, num_clips, output_path):
    video = VideoFileClip(mp4_file)
    mp4_duration = video.duration

    for i in range(num_clips):
        start_time = random.uniform(0, mp4_duration - subclip_duration)
        end_time = start_time + subclip_duration

        subclip = video.subclip(start_time, end_time)

        subclip_path = f"{output_path}\\subclip_{i+1}.mp4"
        subclip.write_videofile(subclip_path, fps=30, preset='ultrafast')

        # throws error i cannot fix.
        # subclip.close()

    video.close()
   
def create_subclips(mp4_file, subclip_duration, output_path):
    video = VideoFileClip(mp4_file)
    mp4_duration = video.duration

    num_clips = int(mp4_duration / subclip_duration)

    for i in range(num_clips):
        start_time = i * subclip_duration
        end_time = start_time + subclip_duration

        subclip = video.subclip(start_time, end_time)

        subclip_path = f"{output_path}\\subclip_{i+1}.mp4"
        subclip.write_videofile(subclip_path, fps=30, preset='ultrafast')

        # throws error i cannot fix.
        # subclip.close()


    video.close()





# Example usage
subclip_duration = 5  # Duration of each subclip in seconds
num_clips = 50
category = "spongebob"
path = f"resources\\background_videos\\memes\\{category}"
mp4_file = f"{path}\\{category}.mp4"
output_path = path
# create_subclips(mp4_file, subclip_duration, output_path)
create_random_subclips(mp4_file, subclip_duration, num_clips, output_path)
