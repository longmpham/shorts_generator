import os
import csv
import random
import time
from moviepy.editor import *
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
import numpy as np

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
    uploaded_videos_folder_path = os.path.join("resources", "uploaded_videos", goal_name)
    _create_folder_if_not_exists(uploaded_videos_folder_path)
    uploaded_videos2_folder_path = os.path.join("resources", "uploaded_videos", goal_name, "uploaded")
    _create_folder_if_not_exists(uploaded_videos2_folder_path)

def get_csv(csv_filename):
    data = []
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Get the header row
        # print("Header:", header)  # Debugging statement
        for row in csv_reader:
            item = {}
            # print("Row:", row)  # Debugging statement
            for i, column in enumerate(header):
                item[column] = row[i]
            data.append(item)
    return data

def get_video_file(goal_name):
    background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", f"{goal_name}")
    background_video_files = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    
    # Ensure unique random choices by shuffling the list
    random.shuffle(background_video_files)
    
    # Choose the first file in the shuffled list
    background_video_file = os.path.join(background_video_dir, background_video_files[0])

    return background_video_file

def get_audio_file(goal_name):
    background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{goal_name}")
    background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]

    # Ensure unique random choices by shuffling the list
    random.shuffle(background_audio_files)

    # Choose the first file in the shuffled list
    background_audio_file = os.path.join(background_audio_dir, background_audio_files[0])

    return background_audio_file


def create_text_label(text, font_size, font_color, bg_color, size, padding=10):
    # Create a blank image with a transparent black background
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate the text dimensions
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position to center the text
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2

    # Calculate the bounding box with padding
    box_x1 = text_x - padding
    box_y1 = text_y - padding
    box_x2 = text_x + text_width + padding
    box_y2 = text_y + text_height + padding

    # Draw a filled rectangle for the text region
    draw.rectangle([(box_x1, box_y1), (box_x2, box_y2)], fill=bg_color)
    # # Draw a rounded rectangle for the text background
    # draw.rounded_rectangle([(box_x1, box_y1), (box_x2, box_y2)], corner_radius=20, fill=bg_color)

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=font_color)

    return np.array(image)

def create_video_from_csv(csv_data, goal_name):
    # Define video parameters
    clip_duration = 5
    mobile_screen_size = (720, 1280) # portrait aspect ratio for mobile phones
    font = "Arial"
    font_size = 50
    font_color = "white"
    bg_color='black'
    opacity = 0.75
    mobile_text_screen_size = (mobile_screen_size[0]*0.8,mobile_screen_size[1])



    for i, data in enumerate(csv_data):
        # Skip the first column
        column_values = list(data.values())[1:]
        
        # Initialize an empty list to store the text clips
        text_clips = []  

        for j, column_value in enumerate(column_values):
            # Convert the PIL image to a MoviePy text clip/image clip
            # text_clip = ImageClip(create_text_label(column_value, font_size=50, font_color=(255, 255, 255), bg_color=(0, 0, 0), size=mobile_screen_size))
            text_clip = TextClip(column_value, fontsize=font_size, color=font_color, bg_color=bg_color, font=font, size=(mobile_text_screen_size[0], None), method='caption')
            text_clip = text_clip.set_position('center').set_start(j * clip_duration).set_duration(clip_duration).set_opacity(opacity)
            
            # Add the text clip to the list
            text_clips.append(text_clip)

        # Total text duration
        total_duration = len(text_clips) * clip_duration

        # Create the clip for the description
        description_text = f"#{goal_name}"
        description_clip = TextClip(description_text, fontsize=font_size*0.75, color=font_color, bg_color=bg_color, font=font, size=(mobile_text_screen_size[0],None))
        description_clip = description_clip.set_position(("center",0.8), relative=True).set_duration(total_duration).set_opacity(1)

        # Create the background clips
        bg_video_clips = []
        for k, text_clip in enumerate(text_clips):
            bg_video_path = get_video_file(goal_name)
            bg_video_clip = VideoFileClip(bg_video_path, audio=True).loop(clip_duration)
            bg_video_clip = bg_video_clip.set_start(k * clip_duration).set_duration(clip_duration)
            bg_video_clip = bg_video_clip.resize(mobile_screen_size)
            bg_video_clips.append(bg_video_clip)

        # Combine the clips
        final_video = CompositeVideoClip([*bg_video_clips, *text_clips, description_clip])
        final_video = final_video.set_duration(total_duration)

        # Add the audio track to the video
        audio_path = get_audio_file(goal_name)
        audio_clip = AudioFileClip(audio_path).set_duration(total_duration)
        audio_clip = audio_clip.volumex(0.5)
        final_video = final_video.set_audio(audio_clip)

        # Write the video to a file
        fname = f"Dog Facts to Make You Smile - {i+1} #shorts #dog #dogs #happy #fyp #pets"
        filename = os.path.join("resources", "uploaded_videos", f"{goal_name}", f"{fname}.mp4")
        final_video.write_videofile(filename, fps=30, preset='ultrafast')
        # final_video.write_videofile(filename, verbose=True, write_logfile=True)
        break # for debug purposes only to generate 1 video.

def main():
    # Goal name should be equivalent to the csv data file. ie. relationshipgoals == relationshipgoals.csv
    
    # goal_name = "relationshipgoals"
    # goal_name = "fitnessfacts"
    goal_name = "dogfacts"
    # goal_name = "catfacts"

    # make dirs if not existing
    create_folder_if_not_exists(goal_name)

    # read csv file
    csv_file = f"{goal_name}.csv"
    csv_path = os.path.join("resources", "data", csv_file)
    data = get_csv(csv_path) # takes csv with 3 fields, category, statement, and goal
    # pprint(data)
    # create shorts!
    create_video_from_csv(data, goal_name)
    
    return

if __name__ == "__main__":
    main()