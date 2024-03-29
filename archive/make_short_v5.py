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
from coqui_tts import generate_TTS_using_bark, generate_TTS_using_coqui
import shutil
from tqdm import tqdm
from faster_whisper import WhisperModel
from gtts import gTTS
from tiktok_tts_v2 import texttotiktoktts

counter = 0

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

    # Create folder under resources/uploaded_videos
    temp_folder_path = os.path.join("resources", "temp")
    _create_folder_if_not_exists(temp_folder_path)

def get_csv(csv_filename):
    # Read the CSV file and extract the relationship data
    data = []
    with open(csv_filename, 'r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the first row
        for row in csv_reader:
            category, statement, goal = row[:3]
            print(category, statement, goal)
            data.append({'category': category, 'statement': statement, 'goal': goal})
    return data

def get_video_file(goal_name):
    # background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", f"{goal_name}")
    background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", "scraper", "catsdogsanimalspetsvertical", "vertical")
    background_video_files = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    background_video_file = os.path.join(background_video_dir, random.choice(background_video_files))
    return background_video_file

def get_audio_file(audio_type):
    background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{audio_type}")
    background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
    background_audio_file = os.path.join(background_audio_dir, random.choice(background_audio_files))
    return background_audio_file

def get_answer_picture(keyword):
    print(f"getting... {keyword}, not a person but a place or thing, 1080x1920")
    image_path = get_image_from_answer(keyword, description=", not a person but a place or thing, 1080x1920")
    return image_path

def generate_TTS_using_GTTS(sentences):
    def delete_temp_audio(folder_path="resources\\temp\\audio"):
        # If temp folder is found, delete it
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Create the folder
        os.mkdir(folder_path)
        
        return
    
    delete_temp_audio()
    
    # Combine audio files
    silence_time = 3 # seconds
    sample_rate = 16000
    change_speed = True
    audio_speed = 1.2
    change_pitch = True
    octaves = 0.25 # For decreasing, octave can be -0.5, -2 etc.

    output_files = []
    # generate the audio and combine them with a short silence after each sentence
    for i, sentence in tqdm(enumerate(sentences), desc="Generating Speech", total=len(sentences)):
        print(sentence)
        output_file = f"resources\\temp\\audio\\post_text_{i}.wav"
        tts = gTTS(sentence, lang='en')
        tts.save(output_file)
        output_files.append(output_file)

    audio_segment_1 = AudioSegment.from_file(output_files[0])
    audio_segment_2 = AudioSegment.from_file(output_files[1])
    audio_segment_3 = AudioSegment.from_file(output_files[2])
    combined_audio_1 = AudioSegment.silent(duration=3*100, frame_rate=sample_rate)
    combined_audio_2 = AudioSegment.silent(duration=1*100, frame_rate=sample_rate)
    # combined_audio_1 += audio_segment_1.set_frame_rate(sample_rate)
    # combined_audio_2 += audio_segment_2.set_frame_rate(sample_rate)
    combined_audio_1 = audio_segment_1.set_frame_rate(sample_rate) + combined_audio_1
    combined_audio_2 = audio_segment_2.set_frame_rate(sample_rate) + combined_audio_2
    
    # Speed audio up
    if(change_speed):
        combined_audio_1 = combined_audio_1.speedup(playback_speed=audio_speed)
        combined_audio_2 = combined_audio_2.speedup(playback_speed=audio_speed)
        audio_segment_3 = audio_segment_3.speedup(playback_speed=audio_speed)
    
    # pitch
    if(change_pitch):
        new_sample_rate = int(combined_audio_1.frame_rate * (2.0 ** octaves))
        combined_audio_1 = combined_audio_1._spawn(combined_audio_1.raw_data, overrides={'frame_rate': new_sample_rate})
        new_sample_rate = int(combined_audio_2.frame_rate * (2.0 ** octaves))
        combined_audio_2 = combined_audio_2._spawn(combined_audio_2.raw_data, overrides={'frame_rate': new_sample_rate})
        new_sample_rate = int(audio_segment_3.frame_rate * (2.0 ** octaves))
        audio_segment_3 = audio_segment_3._spawn(audio_segment_3.raw_data, overrides={'frame_rate': new_sample_rate})

    
    # Export combined audio to file
    # output_file = "resources\\temp\\audio\\post_text.wav"
    combined_audio_1.export("resources\\temp\\audio\\post_text_0.wav", format="wav")
    combined_audio_2.export("resources\\temp\\audio\\post_text_1.wav", format="wav")
    audio_segment_3.export("resources\\temp\\audio\\post_text_2.wav", format="wav")

    return output_files

def generate_TTS_using_TikTok(sentence):
    global counter
    
    path = os.getcwd() + "\\resources\\temp\\audio"
    success, tts_file = texttotiktoktts(sentence, "en_us_001", path, file_name=f"audio_tts_{counter}")
    counter += 1
    
    if not success: exit()
    return tts_file

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

def generate_srt_from_audio_using_whisper(audio_file_path):
    
    def format_timedelta(seconds):
        delta = timedelta(seconds=seconds)
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds % 60
        milliseconds = delta.microseconds // 1000
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f},{milliseconds:03.0f}"
    
    # use large-v2 model and transcribe the audio file
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # print(audio_file_path)
    segments, info = model.transcribe(audio_file_path, beam_size=5)
    segments = list(segments)
    # segments, _ = model.transcribe(
    #     "audio.mp3",
    #     vad_filter=True,
    #     vad_parameters=dict(min_silence_duration_ms=500), # Vad takes out periods of silence
    # )
    # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Create the SRT file path dynamically
    audio_file_name = os.path.basename(audio_file_path)
    srt_file_name = os.path.splitext(audio_file_name)[0] + ".srt"
    srt_file_path = os.getcwd() + f"\\resources\\temp\\{srt_file_name}"
    
    # open a new srt file and save the output from each segment
    with open(srt_file_path, "w") as srt_file:
        # Write each segment to the SRT file
        for index, segment in enumerate(segments, start=1):
        # for index, segment in tqdm(enumerate(segments, start=1), desc="Writing SRT", total=len(segments)):
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, censor_keywords(segment.text)))
            srt_file.write(f"{index}\n")
            # srt_file.write(f"{segment.start:.2f} --> {segment.end:.2f}\n")
            srt_file.write(f"{format_timedelta(segment.start)} --> {format_timedelta(segment.end)}\n")
            srt_file.write(f"{segment.text}\n\n")
    
    return srt_file_path

def add_text_clip(text="", font_name="Impact", font_size=50, font_color="white", bg_color="black", size=(int(720*0.9),None), method="caption", start=0, total_duration=5, opacity=1.0, position=("center"), relative=False):
    text_clip = TextClip(text, fontsize=font_size, color=font_color, bg_color=bg_color, font=font_name, size=size, method=method)
    if relative==True:
        text_clip = text_clip.set_position(position, relative=True).set_start(start).set_duration(total_duration).set_opacity(opacity)
    else:   
        text_clip = text_clip.set_position(position).set_start(start).set_duration(total_duration).set_opacity(opacity)
    return text_clip

def add_video_clip(path, start=0, total_duration=5, size=(720,1280)):
    video_file = get_video_file(path)
    video_clip = VideoFileClip(video_file, audio=True).loop(total_duration)
    video_clip = video_clip.set_start(start).set_duration(total_duration).resize(size)
    return video_clip

def add_audio_tts_clip(audio_file, silence=1, start=0):
    audio_clip = AudioFileClip(audio_file)
    clip_duration = audio_clip.duration + silence
    audio_clip = audio_clip.set_start(start)
    
    return audio_clip, clip_duration

def create_video_from_csv(csv_data, goal_name, description_text, mp4_file_name):
    # Define video parameters
    audio_type = "happy"
    mobile_screen_size = (720, 1280) # portrait aspect ratio for mobile phones
    text_color = "white"
    bg_color='black'
    opacity = 0.75
    mobile_text_screen_size = (mobile_screen_size[0]*0.8,mobile_screen_size[1])
    ending_text = "Sub, Comment, Like for More!"
    
    for i, data in enumerate(csv_data, start=323):
        question_num = data[list(data.keys())[0]]  # Extract the first value dynamically
        question = data[list(data.keys())[1]]  # Extract the second value dynamically
        answer = data[list(data.keys())[2]]  # Extract the third value dynamically
        
        
        # Add the TTS audio track to the video using CompositeAudioClip
        # tts_audio_files = generate_TTS_using_coqui([question, answer])
        # tts_audio_files = generate_TTS_using_GTTS([question, answer, ending_text])
        tts_audio_file1 = generate_TTS_using_TikTok(question)
        tts_audio_file2 = generate_TTS_using_TikTok(answer)
        tts_audio_file3 = generate_TTS_using_TikTok(ending_text)
        tts_audio_clip1, clip1_duration = add_audio_tts_clip(audio_file=tts_audio_file1, silence=2, start=0)
        tts_audio_clip2, clip2_duration = add_audio_tts_clip(audio_file=tts_audio_file2, silence=1, start=clip1_duration)
        tts_audio_clip3, clip3_duration = add_audio_tts_clip(audio_file=tts_audio_file3, silence=0.5, start=clip1_duration+clip2_duration)
        video_duration = clip1_duration + clip2_duration + clip3_duration

        # Create the text clips
        # hashtag_clip = add_text_clip(text=description_text, font_name="Impact", font_size=30, font_color="white", bg_color="black", size=(mobile_text_screen_size[0],None), method="label", start=0, total_duration=video_duration, opacity=1.0, position=("center", 0.8), relative=True)
        question_clip = add_text_clip(text=question, font_name="Impact", font_size=50, font_color="white", bg_color="black", size=(mobile_text_screen_size[0],None), method="caption", start=0, total_duration=clip1_duration, opacity=opacity, position="center")
        answer_clip = add_text_clip(text=answer, font_name="Impact", font_size=50, font_color="white", bg_color="black", size=(mobile_text_screen_size[0],None), method="caption", start=clip1_duration, total_duration=clip2_duration, opacity=opacity, position="center")
        ending_clip = add_text_clip(text=ending_text, font_name="Impact", font_size=50, font_color="white", bg_color="black", size=(mobile_text_screen_size[0],None), method="label", start=clip1_duration + clip2_duration, total_duration=clip3_duration, opacity=1.0, position=("center", 0.1), relative=True)

        # Create the video clips
        bg_question_clip = add_video_clip(path=goal_name, start=0, total_duration=clip1_duration, size=mobile_screen_size)
        bg_answer_clip = add_video_clip(path=goal_name, start=clip1_duration, total_duration=clip2_duration+clip3_duration, size=mobile_screen_size)
        bg_video_full = concatenate_videoclips([bg_question_clip, bg_answer_clip])
        
        # Combine the all the clips
        # final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, hashtag_clip, ending_clip], use_bgclip=True)
        final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, ending_clip], use_bgclip=True)
        final_video = final_video.set_duration(video_duration)

        # Add the audio track to the video
        # background_music
        audio_path = get_audio_file(audio_type)
        audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
        audio_clip = audio_clip.volumex(0.1) # set volume of background_audio to 10%
        
        # mux the audios together
        combined_audio = CompositeAudioClip([audio_clip, tts_audio_clip1, tts_audio_clip2, tts_audio_clip3])
        final_video = final_video.set_audio(combined_audio)
        
        # Write the video to a file
        fname = mp4_file_name.replace("_", str(i+1))
        filename = os.path.join("resources", "uploaded_videos", f"{goal_name}", f"{fname}.mp4")
        # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
        final_video.write_videofile(filename, fps=30, preset='ultrafast')
        # final_video.write_videofile(filename, verbose=True, write_logfile=True)
        
        
        # close clips
        # bg_video_full.close()
        # combined_audio.close()
        
        # break # for debug purposes only to generate 1 video.
        # if i == 3: # generate 3 vids
        #     break

def main():
    
    goal_name = "quiz"
    description_text = "#Jokes"
    mp4_file_name = f"Bet you didnt know this... _ #shorts #quiz #question #animals #pets #dogs #cats #random #fyp" # _ will be replaced by a number

    # Follow the naming convention for csv file:
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
    
# +------------+
# |            |
# |   Title    |
# |            |
# |            |
# |    Text    |
# |            |
# |            |
# |            |
# |            |
# +------------+
