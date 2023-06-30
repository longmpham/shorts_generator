import random
import time
import os
from moviepy.editor import VideoFileClip

def create_random_subclips(mp4_file, output_path, subclip_duration, num_clips):
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
   
def create_subclips(mp4_file, output_path, subclip_duration):
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

def create_subclips_at_time(mp4_file, output_path, subclip_times):
    
    video = VideoFileClip(mp4_file)
    
    for i, (subclip_start, subclip_end) in enumerate(subclip_times):
        subclip = video.subclip(subclip_start, subclip_end)
        subclip_path = f"{output_path}\\subclip_{i}_{subclip_start}-{subclip_end}.mp4"
        subclip.write_videofile(subclip_path, fps=30, preset='ultrafast')

    # subclip = video.subclip(subclip_start, subclip_end)
    # subclip_path = f"{output_path}\\subclip_{subclip_start}-{subclip_end}_.mp4"
    
    subclip.write_videofile(subclip_path, fps=30, preset='ultrafast')
    video.close()
    return

def main():

    # Example usage
    subclip_duration = 5  # Duration of each subclip in seconds
    num_clips = 50
    category = "genshin"
    # path = f"resources\\background_videos\\genshin\\{category}"
    path = f"resources\\background_videos\\{category}"
    mp4_file = f"{path}\\genshin_full.mp4"
    output_path = path
    # create_subclips(mp4_file, output_path, subclip_duration)
    # create_random_subclips(mp4_file, output_path, subclip_duration, num_clips)
    
    
    
    
    
    subclip_times = [
        (0,10),
        (10,20),
        (20,30),
        (30,40),
    ]
    create_subclips_at_time(mp4_file, output_path, subclip_times)
    
    return

if __name__ == "__main__":
    main()