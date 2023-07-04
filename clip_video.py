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
    fname = "4trailer.mp4"
    # path = f"resources\\background_videos\\genshin\\{category}"
    mp4_file_path = f"resources\\background_videos\\genshin\\full"
    input_mp4_file = f"{mp4_file_path}\\{fname}"
    output_path = "resources\\background_videos\\genshin\\trailers"
    # create_subclips(mp4_file, output_path, subclip_duration)
    # create_random_subclips(mp4_file, output_path, subclip_duration, num_clips)

    subclip_times = [
        (188,192),
        # (64,81),
        # (81,95),
        # (103,124),
        # (124,173),
        # (178,208),
        # (132,144),
        # (144,158),
        # (158,173),
        
    ]
    create_subclips_at_time(input_mp4_file, output_path, subclip_times)
    
    return

if __name__ == "__main__":
    main()