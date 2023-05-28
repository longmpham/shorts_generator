import os
import csv
import random
import time
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from get_image import get_image_from_answer
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from datetime import timedelta
import os

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

def get_answer_picture(keyword):
    print(f"getting... {keyword}, not a person but a place or thing, 1080x1920")
    image_path = get_image_from_answer(keyword, description=", not a person but a place or thing, 1080x1920")
    return image_path

def get_audio_file(goal_name):
    background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{goal_name}")
    background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
    background_audio_file = os.path.join(background_audio_dir, random.choice(background_audio_files))
    return background_audio_file

def generate_srt_from_audio(audio_file_path):
    def format_timedelta(milliseconds):
        delta = timedelta(milliseconds=milliseconds)
        seconds = delta.total_seconds()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = delta.total_seconds() * 1000 % 1000
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f},{milliseconds:03.0f}"
    
    # Load the audio file
    audio = AudioSegment.from_file(audio_file_path, format="mp3")

    # Split the audio into smaller chunks
    chunk_length_ms = 10000  # Split audio into 10-second chunks
    chunks = make_chunks(audio, chunk_length_ms)

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Create the SRT file path dynamically
    audio_file_name = os.path.basename(audio_file_path)
    srt_file_name = os.path.splitext(audio_file_name)[0] + ".srt"
    srt_file_path = os.path.join(os.path.dirname(audio_file_path), srt_file_name)

    # Create an SRT file
    with open(srt_file_path, 'w') as srt_file:
        for i, chunk in enumerate(chunks):
            start_time = i * chunk_length_ms
            end_time = (i + 1) * chunk_length_ms

            # Save the chunk as a temporary WAV file
            chunk.export("temp.wav", format="wav")

            # Recognize speech from the temporary WAV file
            with sr.AudioFile("temp.wav") as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            # Write the subtitle to the SRT file
            subtitle = f"{i+1}\n{format_timedelta(start_time)} --> {format_timedelta(end_time)}\n{text}\n\n"
            srt_file.write(subtitle)

    return srt_file_path

def create_video_from_csv(csv_data, goal_name, description_text, mp4_file_name):
    # Define video parameters
    video_duration = 10
    clip1_duration = 7
    clip2_duration = 3
    mobile_screen_size = (720, 1280) # portrait aspect ratio for mobile phones
    text_color = "white"
    bg_color='black'
    opacity = 0.75
    mobile_text_screen_size = (mobile_screen_size[0]*0.8,mobile_screen_size[1])
    
    for i, data in enumerate(csv_data):
        question_num = data[list(data.keys())[0]]  # Extract the first value dynamically
        question = data[list(data.keys())[1]]  # Extract the second value dynamically
        answer = data[list(data.keys())[2]]  # Extract the third value dynamically
        
        # generator = lambda txt: TextClip(txt, font='Arial', fontsize=50, color='white')
        # subs = [((0, 2), 'subs1'),
        #         ((2, 4), 'subs2'),
        #         ((4, 6), 'subs3'),
        #         ((6, 10), 'subs4')]

        # subtitles = SubtitlesClip(subs, generator)
        # subtitles = subtitles.set_position(("center", 0.2))

        question_clip = TextClip(question, fontsize=50, color=text_color, bg_color=bg_color, font='Impact', size=(mobile_text_screen_size[0], None), method='caption')
        question_clip = question_clip.set_position('center').set_start(0).set_duration(clip1_duration).set_opacity(opacity)

        answer_clip = TextClip(answer, fontsize=50, color=text_color, bg_color=bg_color, font='Impact', size=(mobile_text_screen_size[0], None), method='caption')
        answer_clip = answer_clip.set_position('center').set_start(clip1_duration).set_duration(clip2_duration).set_opacity(opacity)

        # Create the clip for the question #
        # question_num_clip = TextClip(f"#{question_num}", fontsize=30, color=text_color, bg_color=bg_color, font='Impact', size=(mobile_text_screen_size[0],None))
        # question_num_clip = question_num_clip.set_position(("top",0.8), relative=True).set_duration(video_duration).set_opacity(1)

        # Create the clip for the description
        hashtag_clip = TextClip(description_text, fontsize=30, color=text_color, bg_color=bg_color, font='Impact', size=(mobile_text_screen_size[0],None))
        hashtag_clip = hashtag_clip.set_position(("center",0.8), relative=True).set_duration(video_duration).set_opacity(1)

        # Create the background clip for question
        bg_video_path = get_video_file(goal_name)
        bg_question_clip = VideoFileClip(bg_video_path, audio=True).loop(clip1_duration)
        bg_question_clip = bg_question_clip.set_start(0).set_duration(clip1_duration)
        bg_question_clip = bg_question_clip.resize(mobile_screen_size)

        # Create the picture clip for answer
        bg_answer_clip = ImageClip(img=get_answer_picture(answer), duration=clip2_duration)
        bg_answer_clip = bg_answer_clip.set_position(("center",0.8), relative=True).set_duration(clip2_duration).set_opacity(1)
        bg_answer_clip = bg_answer_clip.resize(mobile_screen_size)
        
        bg_video_full = concatenate_videoclips([bg_question_clip, bg_answer_clip])
        # bg_video_full = CompositeVideoClip([bg_question_clip, bg_video_clip2])

        # Combine the clips
        # final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, hashtag_clip, subtitles], use_bgclip=True)
        final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, hashtag_clip], use_bgclip=True)
        final_video = final_video.set_duration(video_duration)

        # Add the audio track to the video
        audio_path = get_audio_file(goal_name)
        # audio_path = os.path.join("resources", "audio", f"{goal_name}", f"{goal_name}.mp3")
        audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
        audio_clip = audio_clip.volumex(0.5)
        # audio_clip = AudioFileClip(audio_path).subclip(0, 10)
        final_video = final_video.set_audio(audio_clip)

        # Write the video to a file
        fname = mp4_file_name.replace("_", str(i+1))
        filename = os.path.join("resources", "uploaded_videos", f"{goal_name}", f"{fname}.mp4")
        # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
        final_video.write_videofile(filename, fps=30, preset='ultrafast')
        # final_video.write_videofile(filename, verbose=True, write_logfile=True)
        break # for debug purposes only to generate 1 video.
        # if i == 2: # generate 3 vids
        #     break

def main():
    goal_name = "dadjokes"
    description_text = "#DadJokes"
    mp4_file_name = f"Dad Jokes to Crack You Up - _ #shorts #jokes #jokes #brainteaser #fyp #dadjokes #funny #random #lol #laugh" # _ will be replaced by a number

    # recommend to follow the naming convention:
    # number | question | answer (1 word)

    # make dirs if not existing
    create_folder_if_not_exists(goal_name)

    # read csv file
    csv_file = f"{goal_name}.csv"
    csv_path = os.path.join("resources", "data", csv_file)
    data = get_csv(csv_path) # takes csv with 3 fields, category, statement, and goal

    # create shorts!
    create_video_from_csv(data, goal_name, description_text, mp4_file_name)
    return

if __name__ == "__main__":
    main()