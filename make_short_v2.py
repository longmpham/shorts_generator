import os
import csv
import random
import time
from moviepy.editor import *

def create_folder_if_not_exists(goal_name):

    def _create_folder_if_not_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    data_folder_path = os.path.join("resources", "data")
    _create_folder_if_not_exists(data_folder_path)

    # Create folder under resources/audio
    audio_folder_path = os.path.join("resources", "audio", goal_name)
    _create_folder_if_not_exists(audio_folder_path)

    # Create folder under resources/background_videos
    background_videos_folder_path = os.path.join("resources", "background_videos", goal_name)
    _create_folder_if_not_exists(background_videos_folder_path)

    # Create folder under resources/uploaded_videos
    background_videos_folder_path = os.path.join("resources", "uploaded_videos", goal_name)
    _create_folder_if_not_exists(background_videos_folder_path)

def get_csv(csv_filename):
    # Read the CSV file and extract the relationship data
    data = []
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the first row
        for row in csv_reader:
            category, statement, goal = row[:3]
            data.append({'category': category, 'statement': statement, 'goal': goal})
    return data

def get_video_file(goal_name):
    background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", f"{goal_name}")
    background_video_files  = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    background_video_file = os.path.join(background_video_dir, random.choice(background_video_files))
    return background_video_file

def get_audio_file(goal_name):
    background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{goal_name}")
    background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
    background_audio_file = os.path.join(background_audio_dir, random.choice(background_audio_files))
    return background_audio_file

def create_video_from_csv(csv_data, goal_name):
    # Define video parameters
    video_duration = 10
    clip1_duration = 5
    clip2_duration = 5
    mobile_screen_size = (720, 1280) # portrait aspect ratio for mobile phones
    bg_color='black'
    opacity = 0.75
    mobile_text_screen_size = (mobile_screen_size[0]*0.8,mobile_screen_size[1])
    description_text = f"#{goal_name}"

    # Cycle through all the relationship data, create text clips and join them to a video. Finally add audio
    for i, data in enumerate(csv_data):
        # Create the clip for the statement
        statement_clip = TextClip(data['statement'], fontsize=50, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None))
        statement_clip = statement_clip.set_position('center').set_start(0).set_duration(clip1_duration).set_opacity(opacity)

        # Create the clip for the goal
        goal_clip = TextClip(data['goal'], fontsize=50, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None), method='caption')
        goal_clip = goal_clip.set_position('center').set_start(clip1_duration).set_duration(clip2_duration).set_opacity(opacity)

        # Create the clip for the description
        description_clip = TextClip(description_text, fontsize=30, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None))
        description_clip = description_clip.set_position(("center",0.8), relative=True).set_duration(video_duration).set_opacity(1)

        # Create the background clip 1
        bg_video_path = get_video_file(goal_name)
        bg_video_clip = VideoFileClip(bg_video_path, audio=True).loop(clip1_duration)
        bg_video_clip = bg_video_clip.set_start(0).set_duration(clip1_duration)
        bg_video_clip = bg_video_clip.resize(mobile_screen_size)

        # Create the background clip 2
        bg_video_path2 = get_video_file(goal_name)
        bg_video_clip2 = VideoFileClip(bg_video_path2, audio=True).loop(clip2_duration)
        bg_video_clip2 = bg_video_clip2.set_start(clip1_duration).set_duration(clip2_duration)
        bg_video_clip2 = bg_video_clip2.resize(mobile_screen_size)

        bg_video_full = concatenate_videoclips([bg_video_clip, bg_video_clip2])
        # bg_video_full = CompositeVideoClip([bg_video_clip, bg_video_clip2])

        # Combine the clips
        final_video = CompositeVideoClip([bg_video_full, statement_clip, goal_clip, description_clip], use_bgclip=True)
        final_video = final_video.set_duration(video_duration)

        # Add the audio track to the video
        audio_path = get_audio_file(goal_name)
        # audio_path = os.path.join("resources", "audio", f"{goal_name}", f"{goal_name}.mp3")
        audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
        audio_clip = audio_clip.volumex(0.5)
        # audio_clip = AudioFileClip(audio_path).subclip(0, 10)
        final_video = final_video.set_audio(audio_clip)

        # Write the video to a file
        fname = f"Dog Facts to Make You Smile - {i+1} #shorts #dog #dogs #happy #fyp #pets"
        filename = os.path.join("resources", "uploaded_videos", f"{goal_name}", f"{fname}.mp4")
        # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
        final_video.write_videofile(filename, fps=30, preset='ultrafast')
        # final_video.write_videofile(filename, verbose=True, write_logfile=True)
        # break # for debug purposes only to generate 1 video.

def main():
    # goal_name = "relationshipgoals"
    # goal_name = "fitnessfacts"
    goal_name = "dogfacts"
    # goal_name = "catfacts"
    # csv_file = "relationship_data.csv"

    # make dirs if not existing
    create_folder_if_not_exists(goal_name)

    # read csv file
    csv_file = f"{goal_name}.csv"
    csv_path = os.path.join("resources", "data", csv_file)
    data = get_csv(csv_path) # takes csv with 3 fields, category, statement, and goal

    # create shorts!
    create_video_from_csv(data, goal_name)
    return

if __name__ == "__main__":
    main()