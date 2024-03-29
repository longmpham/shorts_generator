import os
import random
import time
import math
import csv
import datetime
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from skimage.filters import gaussian
# from get_image import get_image_from_answer
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from datetime import timedelta
from coqui_tts import generate_TTS_using_bark, generate_TTS_using_coqui
import shutil
from tqdm import tqdm
from faster_whisper import WhisperModel
from gtts import gTTS
from tiktok_tts_v2 import texttotiktoktts
from natsort import natsorted
from get_reddit_data import get_reddit_data

video_files_list = []
audio_files_list = []

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

def delete_temp_audio(folder_path="resources\\temp\\audio"):
    # If temp folder is found, delete it
    if os.path.exists(folder_path):
        print(f"deleting {folder_path}")
        shutil.rmtree(folder_path)
        print("removed")
    # Create the folder
    os.makedirs(folder_path)
    
    return
    
def get_todays_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d")
    return formatted_date

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

    return

def get_video_files(path):
    global video_files_list
    background_video_dir = os.path.join(os.getcwd(), f"{path}")
    video_files_list = [os.path.join(background_video_dir, f) for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    # video_files_list.sort()  # Sort the video files alphabetically
    video_files_list = natsorted(video_files_list)  # Sort the video files naturally
    # for file in video_files_list:
    #     print(file)
    # exit()
    return video_files_list

def get_video_file(index=-1):
    global video_files_list
    # print(index, len(video_files_list))
    
    if index < 0 or index >= len(video_files_list): 
        print("Video index out of range, using a random video instead!")
        return random.choice(video_files_list)
    
    return video_files_list[index]

# def get_video_file_random(goal_name):
#     background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", f"{goal_name}")
#     background_video_files = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
#     background_video_file = os.path.join(background_video_dir, random.choice(background_video_files))
#     return background_video_file

def get_audio_files(path):
    global audio_files_list
    background_audio_dir = os.path.join(os.getcwd(), f"{path}")
    audio_files_list = [os.path.join(background_audio_dir, f) for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
    # audio_files_list.sort()  # Sort the audio files alphabetically
    audio_files_list = natsorted(audio_files_list)  # Sort the audio files naturally
    # for file in audio_files_list:
    #     print(file)
    # exit()
    return audio_files_list

def get_audio_file(index=-1):
    global audio_files_list
    # print(index, len(audio_files_list))
    
    if index < 0 or index >= len(audio_files_list): 
        print("Audio index out of range, using a random audio instead!")
        rand = random.choice(audio_files_list)
        # return random.choice(audio_files_list)
        return rand
    return audio_files_list[index]

# def get_audio_file(audio_type):
#     background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{audio_type}")
#     background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
#     background_audio_file = os.path.join(background_audio_dir, random.choice(background_audio_files))
#     return background_audio_file

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

def generate_TTS_using_TikTok(sentence, voice=0):
    voices = [
        # ENG VOICES
        "en_us_001",            # 0 Female
        "en_us_006",            # Male 1 # sucks
        "en_us_007",            # Male 2 # better
        "en_us_009",            # Male 3
        "en_us_010",            # Male 4 # best
        "en_male_narration",    # 5
        "en_male_funny",        # 6
        "en_female_emotional",  # 7
        "en_male_cody",         # 8
        
        # DISNEY VOICES
        "en_us_ghostface",          # 9
        "en_us_chewbacca",          # 10
        "en_us_c3po",               # 11
        "en_us_stitch",             # 12
        "en_us_stormtrooper",       # 13
        "en_us_rocket",             # 14
        "en_female_madam_leota",    # 15 # this one is funny.
        "en_male_ghosthost",        # 16
        "en_male_pirate",           # 17 # this one is funny
        
        # UK VOICES
        "en_uk_001", # 18 meh UK voice
        "en_uk_003", # 19 better UK voice
        
        # VOCALS VOICES
        "en_female_f08_salut_damour",       # 20 # Alto
        "en_male_m03_lobby",                # 21 # Tenor
        "en_male_m03_sunshine_soon",        # 22 # Sunshine SOon
        "en_female_f08_warmy_breeze",       # 23 # Warmy Breeze
        "en_female_ht_f08_glorious",        # 24 # Glorious
        "en_male_sing_funny_it_goes_up",    # 25 # It Goes Up
        "en_male_m2_xhxs_m03_silly",        # 26 # Chipmunk
        "en_female_ht_f08_wonderful_world", # 27 # Dramatic
    ]
    
    # create a dynamic path for file generation
    path = os.getcwd() + "\\resources\\temp\\audio"
    existing_files = [f for f in os.listdir(path) if f.startswith("tts_audio_file_")]
    counter = len(existing_files) + 1
    file_name = f"tts_audio_file_{counter}"
    
    # call TikTok API
    success, tts_file = texttotiktoktts(sentence, voices[voice], path, file_name=file_name)
    
    if not success: exit()
    return tts_file

def generate_srt_from_audio_using_whisper(audio_file_path, method="sentence"):
    
    def format_timedelta(seconds):
        delta = timedelta(seconds=seconds)
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds % 60
        milliseconds = delta.microseconds // 1000
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f},{milliseconds:03.0f}"
    
    start = time.time()
    
    # use large-v2 model and transcribe the audio file
    model_size = "large-v3"
    # model = WhisperModel(model_size, device="cpu", compute_type="int8", num_workers=2) # num_workers = default 1
    model = WhisperModel(model_size, device="cuda", compute_type="float16", num_workers=2)
    # print(audio_file_path)
    segments, info = model.transcribe(audio_file_path, beam_size=5, word_timestamps=True)
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
        # for per word srt
        if method == "perword": 
            print("using per word")
            for segment in segments:
                for index, word in enumerate(segment.words):
                    print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
                    srt_file.write(f"{index}\n")
                    # srt_file.write(f"{word.start:.2f} --> {word.end:.2f}\n")
                    srt_file.write(f"{format_timedelta(word.start)} --> {format_timedelta(word.end)}\n")
                    srt_file.write(f"{word.word}\n\n")
        
        # for sentence srt
        elif method == "continuous":
            print("using appending words")
            for segment in segments:
                words = ""
                for index, word in enumerate(segment.words):
                    print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
                    srt_file.write(f"{index}\n")
                    # srt_file.write(f"{word.start:.2f} --> {word.end:.2f}\n")
                    # srt_file.write(f"{format_timedelta(word.start)} --> {format_timedelta(word.end)}\n")
                    if index < len(segment.words) - 1:
                        srt_file.write(f"{format_timedelta(word.start)} --> {format_timedelta(word.end)}\n")
                    else:
                        srt_file.write(f"{format_timedelta(word.start)} --> {format_timedelta(word.end + 2)}\n")
                    srt_file.write(f"{words + word.word}\n\n")
                    words = f"{words}{word.word}"
        else:
            print("using per sentence")
            for index, segment in enumerate(segments, start=1):
            # for index, segment in tqdm(enumerate(segments, start=1), desc="Writing SRT", total=len(segments)):
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
                # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, censor_keywords(segment.text)))
                srt_file.write(f"{index}\n")
                # srt_file.write(f"{segment.start:.2f} --> {segment.end:.2f}\n")
                srt_file.write(f"{format_timedelta(segment.start)} --> {format_timedelta(segment.end)}\n")
                srt_file.write(f"{segment.text}\n\n")
    
    end = time.time()
    
    execution_time = end - start
    print(f"Execution time: {execution_time} seconds")
    
    return srt_file_path




def add_text_clip(text="", font_name="Impact", font_size=50, font_color="white", bg_color="transparent", stroke_color=None, stroke_width=1, size=(int(720*0.9),None), method="caption", start=0, total_duration=5, opacity=1.0, position=("center"), relative=False):
    text_clip = TextClip(text, stroke_color=stroke_color, stroke_width=stroke_width, fontsize=font_size, color=font_color, bg_color=bg_color, font=font_name, size=size, method=method)
    if relative==True:
        text_clip = text_clip.set_position(position, relative=True).set_start(start).set_duration(total_duration).set_opacity(opacity)
    else:   
        text_clip = text_clip.set_position(position).set_start(start).set_duration(total_duration).set_opacity(opacity)
    return text_clip

def add_video_clip(start=0, total_duration=5, size=(720,1280), blur_image=False, crop=False, index=-1):
    
    video_file = get_video_file(index) # -int is random, otherwise, pick a number any number.
    video_clip = VideoFileClip(video_file, audio=True).loop(total_duration)
    
    if crop == True:
        video_clip = video_clip.set_start(start).set_duration(total_duration).resize(height=size[1]).crop(x1=780, width=720, height=1280)
        # resize(height=1920).crop(x_center=960, y_center=960, width=1080, height=1920)
    else: 
        video_clip = video_clip.set_start(start).set_duration(total_duration).resize(size)
    
    def blur(image, blur_level=5):
        """ Returns a blurred (blur_level=radius=3 pixels) version of the image """
        return gaussian(image.astype(float), sigma=blur_level)
    
    if blur_image == True:
        print(f'blurring image because blur is {blur_image}')
        # video_clip = video_clip.fl_image(blur)
        video_clip = video_clip.fl_image(lambda image: blur(image, blur_level=5))
    return video_clip

def add_audio_tts_clip(audio_file, silence=2, start=0):
    # print(audio_file)
    audio_clip = AudioFileClip(audio_file)
    clip_duration = audio_clip.duration + silence
    audio_clip = audio_clip.set_start(start)
    
    return audio_clip, clip_duration

def add_background_audio(final_video, index=-1):    
    audio_path = get_audio_file(index) # random
    background_audio_clip = AudioFileClip(audio_path)
    background_audio_clip = background_audio_clip.volumex(0.1) # set volume of background_audio to 10%
    combined_audio = CompositeAudioClip([background_audio_clip, final_video.audio])
    combined_audio = afx.audio_loop(combined_audio, duration=final_video.duration)
    final_video = final_video.set_audio(combined_audio)
    
    return final_video

def add_audio_bleep():
    
    return


def do_temp():
    # Generate TTS
    # tts_file = generate_TTS_using_TikTok(top_text)
    # tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    tts_file = generate_TTS_using_TikTok("Skill Diff", voice=17)
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    tts_file2 = generate_TTS_using_TikTok("D4 Bad. Hardcore by the way.", voice=17)
    tts_clip2, clip_duration2 = add_audio_tts_clip(tts_file2)
    tts_clip2 = tts_clip2.set_start(9)
    meme_file = "resources\\background_videos\\diablo4\\full\\whirlwind_death.mp4"
    sound_file = "resources\\audio\\soundeffects\\Leave Me Alone Akira Meme.mp3"
    # video_clip = VideoFileClip(meme_file, audio=False).loop(clip_duration)
    video_clip = VideoFileClip(meme_file, audio=False)
    video_clip = video_clip.set_duration(9).resize(height=1280).crop(x1=780, width=720, height=1280)
    

    size = video_clip.size

    text_clip_bottom = add_text_clip(text="Skill Diff", font_size=100, stroke_color="black", stroke_width=1, position=("center", 0.75), relative=True, start=0, total_duration=video_clip.duration+tts_clip2.duration, size=(size[0], None))
  
    # Finally, create the video
    final_video = CompositeVideoClip([video_clip, text_clip_bottom], use_bgclip=True)
        
    # Combine to final video
    audio_clip = AudioFileClip(sound_file)
    audio_clip = audio_clip.subclip(1)
    audio_clip = audio_clip.set_start(3.5)
    audio_clip = audio_clip.volumex(0.75) # set volume of background_audio to 10%
    combined_audio = CompositeAudioClip([audio_clip, tts_clip, tts_clip2])
    # combined_audio = afx.audio_loop(combined_audio, duration=final_video.duration)
    final_video = final_video.set_audio(combined_audio)
    final_video.write_videofile("test.mp4", fps=30, codec='h264_nvenc')
    
    
    exit()
    return

def main():
    delete_temp_audio()
    
    audio_type = "happy" # change this to categories eventually, look up music dmca stuff
    audio_path = f"resources\\audio\\{audio_type}"
    video_path = "resources\\background_videos\\scraper\\catsdogsanimalspetsvertical\\vertical"#scraper\\verticalyoga"
    # video_path = "resources\\uploaded_videos\\daily_tiktoks\\uploaded"
    get_video_files(video_path)
    get_audio_files(audio_path)
    
    do_temp()
    return

if __name__ == "__main__":
    main()
    
# +------------+
# |            |
# |   Title    |
# |            |
# |            |
# |            |
# |            |
# |            |
# |    Text    |
# |            |
# +------------+