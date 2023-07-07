import os
import random
import time
import math
import csv
import datetime
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from skimage.filters import gaussian
from get_image import get_image_from_answer
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
    model_size = "large-v2"
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





def create_video_audio_text_sequential_clip(top_text, bottom_text, crop=False, index=0):
    tts_file = generate_TTS_using_TikTok(bottom_text)
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    
    text_clip_top = None
    if top_text and top_text.strip(): # takes care of None and "" 
        text_clip_top = add_text_clip(text=top_text, position=("center", 0.2), relative=True, start=0, total_duration=clip_duration)
    text_clip_bottom = add_text_clip(text=bottom_text, stroke_color="black", stroke_width=2, position=("center", "center"), relative=True, total_duration=clip_duration)

    # Add background video
    video_clip = add_video_clip(total_duration=clip_duration, crop=crop, index=index)
    
    # Finally, create the video
    if text_clip_top:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom, text_clip_top], use_bgclip=True)
    else:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom], use_bgclip=True)
    final_video = final_video.set_audio(tts_clip)
    
    return final_video

def create_video_audio_text_clip(top_text, bottom_text, crop=False):
    print('generating video...')
    
    # Generate TTS
    # tts_file = generate_a_TTS_using_TikTok(text)
    # tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    tts_file = generate_TTS_using_TikTok(bottom_text)
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    
    # Generate Texts
    text_clip_top = None
    if top_text and top_text.strip(): # takes care of None and "" 
        text_clip_top = add_text_clip(text=top_text, position=("center", 0.2), relative=True, start=0, total_duration=clip_duration)
        
    # text_clip = add_text_clip(text=text, total_duration=clip_duration, bg_color="transparent", position=("center", "center"), relative=True) # original
    # text_clip = add_text_clip(text=text, total_duration=clip_duration, font_name="Montserrat Semibold", bg_color="transparent", stroke_color="black", stroke_width=3, position=("center", "center"), relative=True)
    # text_clip_top = add_text_clip(text=top_text, position=("center", 0.2), relative=True, start=0, total_duration=clip_duration)
    text_clip_bottom = add_text_clip(text=bottom_text, stroke_color="black", stroke_width=2, position=("center", "center"), relative=True, total_duration=clip_duration)
    
    # Add background video
    video_clip = add_video_clip(total_duration=clip_duration, crop=crop) # random
    
    # Finally, create the video
    if text_clip_top:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom, text_clip_top], use_bgclip=True)
    else:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom], use_bgclip=True)
        
    
    # Combine to final video
    # final_video = CompositeVideoClip([video_clip, text_clip_bottom], use_bgclip=True)
    # final_video = CompositeVideoClip([video_clip, text_clip_top, text_clip_bottom], use_bgclip=True)
    final_video = final_video.set_audio(tts_clip)
    
    # close partial clips (audiofileclips and videofileclips)
    # tts_clip.close()
    # video_clip.close()
    
    # Debug
    # filename = "test.mp4"
    # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
    # final_video.write_videofile("test.mp4", fps=30, preset='ultrafast')
    # exit()
    return final_video

def generate_169_video(top_text, bottom_text, crop):
    # if crop == True: size = (1280,720)
    # else: 
    size = (720, 1280)
    
    useSRT = False
    # generate tts
    tts_file = generate_TTS_using_TikTok(bottom_text)
    print("TTS generated!")
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    print("TTS clips done!")
    
    # Generate Texts
    top_text_clip = None
    if top_text and top_text.strip(): # takes care of None and "" 
        top_text_clip = add_text_clip(text=top_text, font_size=100, bg_color="black", opacity=0.7, position=("center", 0.05), relative=True, total_duration=clip_duration, size=(size[0]*0.9,None))
    
    bottom_text_clip = add_text_clip(text=bottom_text, position=("center", "center"), relative=True, total_duration=clip_duration, size=(size[0]*0.9,None), stroke_color="black", stroke_width=1)
    
    # generate SRT (per word)
    if useSRT == True: 
        srt_file = generate_srt_from_audio_using_whisper(tts_file, method="continuous")
        generator = lambda txt: TextClip(txt=txt, fontsize=50, color="white", font="Impact", method="caption", size=(size[0]*0.8, None))
        # generator = lambda txt: add_text_clip(text=txt, position=("center"), total_duration=clip_duration)
        subtitles = SubtitlesClip(srt_file, generator)
        subtitles = subtitles.set_position(("center", "bottom")).set_duration(clip_duration)
        print("Subtitles Set...")    
    
        bottom_text_clip = subtitles

    # generate video clip
    video_clip = add_video_clip(start=0, total_duration=clip_duration, size=size, crop=crop)
    
    # Finally, create the video
    if top_text_clip:
        final_video_clip = CompositeVideoClip([video_clip, top_text_clip, bottom_text_clip], use_bgclip=True)
    else:
        final_video_clip = CompositeVideoClip([video_clip, bottom_text_clip], use_bgclip=True)
        
    # combine text and black bar
    # final_video_clip = CompositeVideoClip([video_clip, top_text_clip, bottom_text_clip], use_bgclip=True)
    final_video_clip = final_video_clip.set_duration(clip_duration)

    # Set Audio
    final_video_clip = final_video_clip.set_audio(tts_clip)
    print("Videos and banner, and TTS set!")

    # Debug
    # final_video_clip.save_frame("frame.png", t=3)
    # exit()
    # final_video_clip.write_videofile(final_video_path)

    # close partial clips (audiofileclips and videofileclips)
    # tts_clip.close()
    # video_clip.close()

    # combined_video.close()
    return final_video_clip

def generate_169_vertical_black_bars_video(top_text, bottom_text, crop):

    size=(1280,720)
    useSRT = True
    # generate tts
    tts_file = generate_TTS_using_TikTok(bottom_text)
    print("TTS generated!")
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    print("TTS clips done!")
    
    
    # generate text
    top_text_clip = add_text_clip(text=top_text, font_size=100, position=("center", "center"), total_duration=clip_duration, size=(size[0]*0.9,None))
    bottom_text_clip = add_text_clip(text=bottom_text, position=("center", "top"), total_duration=clip_duration, size=(size[0]*0.9,None))
    
    # generate SRT (per word)
    if useSRT == True: 
        srt_file = generate_srt_from_audio_using_whisper(tts_file, method="continuous")
        generator = lambda txt: TextClip(txt=txt, fontsize=50, color="white", font="Impact", method="caption", size=(size[0]*0.8, None))
        # generator = lambda txt: add_text_clip(text=txt, position=("center"), total_duration=clip_duration)
        subtitles = SubtitlesClip(srt_file, generator)
        subtitles = subtitles.set_position(("center", "top")).set_duration(clip_duration)
        print("Subtitles Set...")    
    
        bottom_text_clip = subtitles
    
    # generate black bars (top and bottom)
    black_image_path = "resources\\black_image.png"
    top_black_bar = ImageClip(black_image_path).set_duration(clip_duration).set_position(("center","top")).resize(size)
    bottom_black_bar = ImageClip(black_image_path).set_duration(clip_duration).set_position(("center","bottom")).resize(size)

    # generate video clip
    video_clip = add_video_clip(start=0, total_duration=clip_duration, size=size, crop=crop)

    # combine text and black bar
    final_top_video_text_clip = CompositeVideoClip([top_black_bar, top_text_clip])
    final_top_video_text_clip = final_top_video_text_clip.set_duration(clip_duration)
    final_bottom_video_text_clip = CompositeVideoClip([bottom_black_bar, bottom_text_clip])
    final_bottom_video_text_clip = final_bottom_video_text_clip.set_duration(clip_duration)

    # create the entire clip
    combined_video = clips_array([[final_top_video_text_clip], [video_clip], [final_bottom_video_text_clip]])
    
    # Set Audio
    combined_video = combined_video.set_audio(tts_clip)
    # combined_video.save_frame("frame.png", t=1)
    # combined_video.write_videofile(final_video_path)
    print("Videos and banner, and TTS set!")

    # close partial clips (audiofileclips and videofileclips)
    # tts_clip.close()
    # video_clip.close()

    # combined_video.close()
    return combined_video

def create_video_from_csv(csv_type, csv_data, mp4_file_name):
    
    ending_text = "Sub, Comment, Like for More!"
    
    # iterate through the CSV data
    for i, data in enumerate(csv_data, start=0):
        # get csv data fields per row
        question_num = data[list(data.keys())[0]]  # Extract the first value dynamically
        question = data[list(data.keys())[1]]  # Extract the second value dynamically
        answer = data[list(data.keys())[2]]  # Extract the third value dynamically
        
        # generate TTS files and TTS Clips
        tts_audio_file1 = generate_TTS_using_TikTok(question)
        tts_audio_file2 = generate_TTS_using_TikTok(answer)
        tts_audio_file3 = generate_TTS_using_TikTok(ending_text)
        tts_audio_clip1, clip1_duration = add_audio_tts_clip(audio_file=tts_audio_file1, silence=2, start=0)
        tts_audio_clip2, clip2_duration = add_audio_tts_clip(audio_file=tts_audio_file2, silence=1, start=clip1_duration)
        tts_audio_clip3, clip3_duration = add_audio_tts_clip(audio_file=tts_audio_file3, silence=0.5, start=clip1_duration+clip2_duration)
        video_duration = clip1_duration + clip2_duration + clip3_duration        
        
        # generate the texts for the video
        # hashtag_clip = add_text_clip(text=description_text, font_name="Impact", font_size=30, font_color="white", bg_color="black", method="label", start=0, total_duration=video_duration, opacity=1.0, position=("center", 0.8), relative=True)
        question_clip = add_text_clip(text=question, font_name="Impact", font_size=50, font_color="white", stroke_color="black", method="caption", start=0, total_duration=clip1_duration, opacity=0.8, position="center")
        answer_clip = add_text_clip(text=answer, font_name="Impact", font_size=50, font_color="white", stroke_color="black", method="caption", start=clip1_duration, total_duration=clip2_duration, opacity=0.8, position="center")
        ending_clip = add_text_clip(text=ending_text, font_name="Impact", font_size=50, font_color="white", stroke_color="black", method="label", start=clip1_duration + clip2_duration, total_duration=clip3_duration, opacity=1.0, position=("center", "center"), relative=True)
        title_clip = add_text_clip(text="#LifeProTips", font_name="Impact", font_size=50, font_color="white", bg_color="black", method="label", start=0, total_duration=video_duration, opacity=1.0, position=("center", 0.1), relative=True)

        # generate the video clips
        bg_question_clip = add_video_clip(start=0, total_duration=clip1_duration)
        bg_answer_clip = add_video_clip(start=clip1_duration, total_duration=clip2_duration+clip3_duration)
        bg_video_full = concatenate_videoclips([bg_question_clip, bg_answer_clip])
                
        # Combine the all the clips
        # final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, hashtag_clip, ending_clip], use_bgclip=True)
        final_video = CompositeVideoClip([bg_video_full, question_clip, answer_clip, ending_clip, title_clip], use_bgclip=True)
        final_video = final_video.set_duration(video_duration)        
        
        # background_music
        audio_path = get_audio_file()
        audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
        audio_clip = audio_clip.volumex(0.1) # set volume of background_audio to 10%
        
        # mux the audios together
        combined_audio = CompositeAudioClip([audio_clip, tts_audio_clip1, tts_audio_clip2, tts_audio_clip3])
        final_video = final_video.set_audio(combined_audio)
        
        # Write the video to a file
        fname = mp4_file_name.replace("_", str(i+1))
        filename = os.path.join("resources", "uploaded_videos", f"{csv_type}", f"{fname}.mp4")
        # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
        final_video.write_videofile(filename, fps=30, preset='ultrafast')
        # final_video.write_videofile(filename, verbose=True, write_logfile=True)
        
        
        # close clips
        # bg_video_full.close()
        # combined_audio.close()
        
        # break # for debug purposes only to generate 1 video.
        # if i == 3: # generate 3 vids
        #     break        
        
    
    return

def generate_meme_video(top_text, bottom_text, meme_file, tts_voice_index=0):
    # Generate TTS
    text = f"{top_text}, {bottom_text}"
    # tts_file = generate_TTS_using_TikTok(top_text)
    # tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    tts_file = generate_TTS_using_TikTok(text, voice=tts_voice_index)
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    
    video_clip = VideoFileClip(meme_file, audio=True).loop(clip_duration)

    size = video_clip.size

    # Generate Texts
    text_clip_top = None
    if top_text and top_text.strip(): # takes care of None and "" 
        text_clip_top = add_text_clip(text=top_text, font_size=30, stroke_color="black", stroke_width=1, position=("center", 0.05), relative=True, start=0, total_duration=clip_duration, size=(size[0], None))
        
    text_clip_bottom = add_text_clip(text=bottom_text, font_size=30, stroke_color="black", stroke_width=1, position=("center", 0.75), relative=True, start=0, total_duration=clip_duration, size=(size[0], None))
    
    # generate SRT (per word)
    useSRT = True
    if useSRT == True: 
        srt_file = generate_srt_from_audio_using_whisper(tts_file, method="perword")
        generator = lambda txt: TextClip(txt=txt, fontsize=30, color="white", font="Impact", stroke_color="black", method="caption", size=(size[0]*0.9, None))
        # generator = lambda txt: add_text_clip(text=txt, position=("center"), total_duration=clip_duration)
        subtitles = SubtitlesClip(srt_file, generator)
        subtitles = subtitles.set_position(("center", "bottom")).set_duration(clip_duration)
        print("Subtitles Set...")    
    
        text_clip_bottom = subtitles
    
    
    # Add background video
    
    # text_clip_bottom = TextClip("hello world", size=size)
    # text_clip_bottom = text_clip_bottom.set_duration(clip_duration).set_position(("center", "bottom"), relative=True)
    
    # Finally, create the video
    if text_clip_top:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom, text_clip_top], use_bgclip=True)
    else:
        final_video = CompositeVideoClip([video_clip, text_clip_bottom], use_bgclip=True)
        
    # Combine to final video
    final_video = final_video.set_audio(tts_clip)
    final_video.write_videofile("test.mp4", fps=30, preset='ultrafast')

    
    # close partial clips (audiofileclips and videofileclips)
    # tts_clip.close()
    # video_clip.close()
    
    # Debug
    # filename = "test.mp4"
    # final_video.save_frame("frame.png", t=1)
    # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
    # final_video.write_videofile("test.mp4", fps=30, preset='ultrafast')
    # exit()
    return final_video

def generate_reddit_video(num_posts=10, num_comments=3, crop=False):
    
    def make_sentences(post, num_comments=3):
        sentences = []
        post_author = post["author"]
        post_title = post["title"]
        post_body = post["selftext"]
        post_comments = post["comments"]
    
        sentences.append(f"{post_author} said {post_title}")
        if post_body.strip() and len(post_body.split()) < 10:
            sentences.append(post_body)
    
        # Generate Textclips for the comments
        for i, post_comment in enumerate(post_comments):
            comment_author = post_comment["author"]
            comment_body = post_comment["comment"]
            
            word_count = len(comment_body.split())
            if word_count > 20:
                continue
            
            sentences.append(f"{comment_author} said {comment_body}")
            if len(sentences) >= num_comments:
                break

        sentences.append("Sub, Comment, Like for More!")
    
        return sentences
    
    size = (720, 1280)
    useSRT = True
    crop = crop # False if using vertical videos, True if using landscape to crop.
    
    # Get each post for each post that comes back
    url = "https://www.reddit.com/r/Ask/top.json?t=day"
    posts = get_reddit_data(url=url, num_posts=num_posts)
    for i, post in enumerate(posts): 
        
        # 
        start_time = time.time()
        
        # Generate sentences to break up the chunks
        sentences = make_sentences(post, num_comments)

        # for each sentence, make a TTS, video and merge them
        video_clips = []
        for sentence in sentences:
            print(sentence)
            tts_file = generate_TTS_using_TikTok(sentence)
            tts_clip, clip_duration = add_audio_tts_clip(tts_file)

            # Generate TextClips
            title = post['title']
            text_clip_title = add_text_clip(text=title, bg_color="black", opacity=0.8, position=("center", 0.1), relative=True, total_duration=clip_duration, size=(size[0]*0.9,None))
            # text_clips.append(text_clip_title) # intro text
        
            # text_clips = []
            text_clip_body = add_text_clip(text=sentence, font_size=40, position=("center", "center"), relative=True, total_duration=clip_duration, size=(size[0]*0.9,None), stroke_color="black", stroke_width=1)
            # text_clips.append(text_clip_body)
            
            # generate SRT (per word)
            if useSRT == True: 
                srt_file = generate_srt_from_audio_using_whisper(tts_file, method="continuous")
                generator = lambda txt: TextClip(txt=txt, fontsize=40, color="white", font="Impact", stroke_color="black", method="caption", size=(size[0]*0.9, None))
                # generator = lambda txt: add_text_clip(text=txt, position=("center"), total_duration=clip_duration)
                subtitles = SubtitlesClip(srt_file, generator)
                subtitles = subtitles.set_position(("center", "center")).set_duration(clip_duration)
                print("Subtitles Set...")
            
                text_clip_body = subtitles

            # generate video clip
            video_clip = add_video_clip(start=0, total_duration=clip_duration, size=size, crop=crop)
            
            # Finally, create the video
            final_video_clip = CompositeVideoClip([video_clip, text_clip_body, text_clip_title], use_bgclip=True)
            final_video_clip = final_video_clip.set_duration(clip_duration)

            # Set Audio
            final_video_clip = final_video_clip.set_audio(tts_clip)
            print("Videos and banner, and TTS set!")

            # Debug
            # final_video_clip.save_frame("frame.png", t=3)
            # exit()
            # final_video_clip.write_videofile(final_video_path)

            # close partial clips (audiofileclips and videofileclips)
            # tts_clip.close()
            # video_clip.close()

            # combined_video.close()
            video_clips.append(final_video_clip)
        
        final_video = concatenate_videoclips(video_clips)
        # Set the background audio music
        final_video = add_background_audio(final_video)

        # Write the final video
        title = f"reddit_{i}"
        # final_video.save_frame("frame.png", t=1)
        # exit()
        final_video.write_videofile(f"{title}.mp4", fps=30, preset='ultrafast')
        
        final_video.close()      
        
        end_time = time.time()  
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

def generate_full_length_video(sentences, mp4_file, tts_voice_index):
    
    video_clip = VideoFileClip(mp4_file, audio=True)
    
    size = video_clip.size
    
    total_duration = 0
    tts_clips = []
    text_clips = []
    for sentence in sentences:
        # Generate TTS
        tts_file = generate_TTS_using_TikTok(sentence, voice=tts_voice_index)
        tts_clip, clip_duration = add_audio_tts_clip(tts_file, silence=0)
        tts_clips.append(tts_clip)
        
        # Generate Texts
        print(f"the start is {total_duration} and the end is {total_duration+clip_duration}")
        # text_clip = add_text_clip(text=sentence, font_size=40, stroke_color="black", stroke_width=1, position=("center", 0.75), relative=True, start=total_duration, total_duration=total_duration+clip_duration, size=(size[0], None))
        text_clip = TextClip(sentence, font="Impact",fontsize=40, color="white", stroke_color="black", stroke_width=1, size=(size[0], None), method="caption")
        text_clip = text_clip.set_position(("center", 0.75), relative=True).set_start(total_duration).set_end(total_duration+clip_duration)
        text_clips.append(text_clip)

        total_duration += clip_duration
    
    text_clips[-1] = text_clips[-1].set_end(video_clip.duration)

    if float(video_clip.duration) < float(total_duration):
        video_clip = VideoFileClip(mp4_file, audio=True).loop(total_duration)

    final_video = CompositeVideoClip([video_clip, *text_clips], use_bgclip=True)
    final_video = final_video.set_duration(video_clip.duration)
        
    # Combine to final video
    audio = concatenate_audioclips(tts_clips)
    final_video = final_video.set_audio(audio)
    
    # Set the background audio music
    final_video = add_background_audio(final_video)

    # Write the final video
    final_video.write_videofile("test.mp4", fps=30, preset='ultrafast')
        
    return

def main():
    delete_temp_audio()
    
    audio_type = "happy" # change this to categories eventually, look up music dmca stuff
    audio_path = f"resources\\audio\\{audio_type}"
    video_path = "resources\\background_videos\\quiz"#scraper\\verticalyoga"
    get_video_files(video_path)
    get_audio_files(audio_path)
    
    # today = get_todays_date()
    
    title = f"Some title" # must be blank if no title is needed!!!
    texts = [
        "Could this be the next archon in Genshin?",

        "Sub, Comment, Like for More!",
    ]
    crop = False
    use_title = False
    mode = 6
    # 0, # vertical, 
    # 1, # 16:9 vertical black bars, requires top and bottom text
    # 2, # 16:9 vertical video, requires top and bottom text and crop
    # 3, # sequential, requires more setup such as organizing video data and audio data (alphanumeric sorted)
    # 4, # from csv, csv file required
    # 5, # a gif in vertical format
    # 6, # reddit. It calls reddit, builds the list, no input necessary other than the video library (crop or not)
    # 7, # Play an entire video clip with text in the back, tts, and audio bg
    
    if mode == 7:
        
        meme_file = "alternative_garbage_can.mp4"
        meme_path = os.path.join(os.getcwd(), "resources", "background_videos", "memes", f"{meme_file}")
        text = ["When you know she's a keeper", 
                "and if you like her a lot", 
                "ask her out.", 
                "You won't regret it.", 
                "The worst she can say is 'no'", 
                "The best she can say is 'yes'", 
                "You've got this.",
            ]
        tts_voice_index = 0 # 17 is ok, 9 is ok
        generate_full_length_video(text,meme_path, tts_voice_index)
        return
    
    if mode == 6:
        generate_reddit_video(num_posts=10, num_comments=3, crop=crop)
        return
    
    if mode == 5: 
        # these are for quick 3-6 second gifs, text doesn't change or anything.
        meme_file = "alternative_garbage_can.mp4"
        meme_path = os.path.join(os.getcwd(), "resources", "background_videos", "memes", f"{meme_file}")
        top_text = ""
        bottom_text = "some text"
        tts_voice_index = 0 # 17 is ok, 9 is ok
        generate_meme_video(top_text, bottom_text, meme_path, tts_voice_index)
        return
    
    if mode == 4:
        file_name = f"Life Pro Tips You Should know #shorts #fyp #lifeprotips #tips #random #mental #strong #health _" # _ will be replaced by number
        csv_type = "lpt"
        csv_file = f"{csv_type}.csv"
        csv_path = os.path.join("resources", "data", csv_file)
        csv_data = get_csv(csv_path) # takes csv with 3 fields, category, statement, and goal
        create_video_from_csv(csv_type, csv_data, file_name)
        return
    
    # should hide this logic and throw in a function... we'll decide later
    video_clips = []
    for i, bottom_text in enumerate(texts):
        if mode == 0:
            video = create_video_audio_text_clip(title, bottom_text, crop=crop)
        elif mode == 1: 
            video = generate_169_vertical_black_bars_video(title, bottom_text, crop=crop)
        elif mode == 2:
            if use_title == False:
                if i >= 1: 
                    title = ""
            video = generate_169_video(title, bottom_text, crop=crop)
        else: 
            video = create_video_audio_text_sequential_clip(title, bottom_text, crop=crop, index=i+1)
        video_clips.append(video)
    final_video = concatenate_videoclips(video_clips)
    
    # Set the background audio music
    final_video = add_background_audio(final_video)

    # Write the final video
    if title=="": title = "yt_short"
    # final_video.save_frame("frame.png", t=1)
    # exit()
    final_video.write_videofile(f"{title}.mp4", fps=30, preset='ultrafast')
    
    final_video.close()
    # background_audio_clip.close()
    # combined_audio.close()
    for clip in video_clips:
        clip.close()

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