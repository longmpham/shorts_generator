import random
import time
import os
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

def create_random_subclips(mp4_file, output_path, subclip_duration, num_clips):
    video = VideoFileClip(mp4_file)
    mp4_duration = video.duration

    for i in range(num_clips):
        start_time = random.uniform(0, mp4_duration - subclip_duration)
        end_time = start_time + subclip_duration

        subclip = video.subclip(start_time, end_time)

        subclip_path = f"{output_path}\\subclip_{i+1}.mp4"
        subclip.write_videofile(subclip_path, fps=30, codec='h264_nvenc')

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
        subclip.write_videofile(subclip_path, fps=30, codec='h264_nvenc')

        # throws error i cannot fix.
        # subclip.close()


    video.close()

def create_audio_subclips_at_time(mp3_file, output_path, subclip_times):
    
    audio = AudioFileClip(mp3_file)
    print(audio)
    for i, (subclip_start, subclip_end) in enumerate(subclip_times):
        subclip = audio.subclip(subclip_start, subclip_end)
        subclip_path = f"{output_path}\\subclip_{i}_{subclip_start}-{subclip_end}.wav"
        subclip.write_audiofile(subclip_path)

    # subclip = video.subclip(subclip_start, subclip_end)
    # subclip_path = f"{output_path}\\subclip_{subclip_start}-{subclip_end}_.mp4"
    
    # subclip.write_audiofile(subclip_path, fps=30, codec='h264_nvenc')
    audio.close()
    return

def create_subclips_at_time(mp4_file, output_path, subclip_times):
    
    video = VideoFileClip(mp4_file)
    
    for i, (subclip_start, subclip_end) in enumerate(subclip_times):
        subclip = video.subclip(subclip_start, subclip_end)
        subclip_path = f"{output_path}\\subclip_{i}_{subclip_start}-{subclip_end}.mp4"
        subclip.write_videofile(subclip_path, fps=30, codec='h264_nvenc')

    # subclip = video.subclip(subclip_start, subclip_end)
    # subclip_path = f"{output_path}\\subclip_{subclip_start}-{subclip_end}_.mp4"
    
    # subclip.write_videofile(subclip_path, fps=30, codec='h264_nvenc')
    video.close()
    return

def main():

    # Example usage
    subclip_duration = 5  # Duration of each subclip in seconds
    num_clips = 50
    fname = "Most Popular Song Each Month in the 2000s.mp3"
    # path = f"resources\\background_videos\\genshin\\{category}"
    mp3_file_path = f"resources\\audio\\songs"
    input_mp3_file = f"{mp3_file_path}\\{fname}"
    output_path = "resources\\audio\\songs\\clips"
    
    # mp4_file_path = f"resources\\background_videos\\diablo4\\full"
    # input_mp4_file = f"{mp4_file_path}\\{fname}"
    # output_path = "resources\\background_videos\\diablo4\\full"
    # create_subclips(mp4_file, output_path, subclip_duration)
    # create_random_subclips(mp4_file, output_path, subclip_duration, num_clips)

    subclip_times = [
        (110,115),
        
    ]
    create_audio_subclips_at_time(input_mp3_file, output_path, subclip_times)
    # create_subclips_at_time(input_mp4_file, output_path, subclip_times)
    
    return

if __name__ == "__main__":
    main()
    
        # (5,10),
        # (11,17),
        # (18,24),
        # (25,30),
        # (30,35),
        # (37,43),
        # (44,50),
        # (52,57),
        # (58,62),
        # (64,70),
        # (71,76),
        # (78,84),
        # (85,89),
        # (90,96),
        # (98,102),
        # (103,108),