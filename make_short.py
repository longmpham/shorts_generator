import os
import csv
import random
from moviepy.editor import *


def get_csv(csv_filename):
    # Read the CSV file and extract the relationship data
    relationship_data = []
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the first row
        for row in csv_reader:
            gender, statement, goal = row[:3]
            relationship_data.append({'gender': gender, 'statement': statement, 'goal': goal})
    return relationship_data

def get_video_file():
    background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos")
    background_video_files  = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    background_video_file = os.path.join(background_video_dir, random.choice(background_video_files))
    return background_video_file

def create_relationship_video(relationship_data):
    # Define video parameters
    video_duration = 10
    clip1_duration = 8
    clip2_duration = 2
    mobile_screen_size = (720, 1280) # portrait aspect ratio for mobile phones
    bg_color='black'
    opacity = 0.75
    mobile_text_screen_size = (mobile_screen_size[0]*0.8,mobile_screen_size[1])
    

    # Cycle through all the relationship data, create text clips and join them to a video. Finally add audio
    for i, data in enumerate(relationship_data):
        # Create the clip for the statement
        statement_clip = TextClip(data['statement'], fontsize=40, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None))
        statement_clip = statement_clip.set_position('center').set_start(0).set_duration(clip1_duration).set_opacity(opacity)
                
        # Create the clip for the goal
        goal_clip = TextClip(data['goal'], fontsize=40, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None), method='caption')
        goal_clip = goal_clip.set_position('center').set_start(clip1_duration).set_duration(clip2_duration).set_opacity(opacity)
        
        # Create the clip for the description
        description_clip = TextClip("#relationshipgoals", fontsize=30, color='white', bg_color=bg_color, font='Arial', size=(mobile_text_screen_size[0],None))
        description_clip = description_clip.set_position(("center",0.8), relative=True).set_duration(video_duration).set_opacity(1)

        # Create the background clip
        bg_video_path = get_video_file()
        bg_video_clip = VideoFileClip(bg_video_path, audio=True).loop(10)
        bg_video_clip = bg_video_clip.set_start(0).set_duration(video_duration)
        bg_video_clip = bg_video_clip.resize(mobile_screen_size)
        
        # Combine the audio and video
        # combined_clip = bg_video_clip.set_audio(audio_clip)

        # Combine the clips
        final_video = CompositeVideoClip([bg_video_clip, statement_clip, goal_clip, description_clip], use_bgclip=True)
        final_video = final_video.set_duration(video_duration)

        # Add the audio track to the video
        audio_path = os.path.join("resources", "audio", "inspiring-emotional-uplifting-piano.mp3")
        audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
        audio_clip = audio_clip.volumex(0.5)
        # audio_clip = AudioFileClip(audio_path).subclip(0, 10)
        final_video = final_video.set_audio(audio_clip)
        
        # Write the video to a file
        filename = os.path.join("resources", "uploaded_videos", f"{data['gender']}_relationship_video_{i+1}.mp4")
        # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
        final_video.write_videofile(filename, verbose=True, write_logfile=True)
        break

def main():
    csv_path = os.path.join("resources", "data", "relationship_data.csv")

    # get a list of gender, statement, goal and return to relationship_lines
    relationship_lines = get_csv(csv_path)
    create_relationship_video(relationship_lines)

    return

if __name__ == "__main__":
    main()