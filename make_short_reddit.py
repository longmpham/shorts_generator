import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" # for whatever reason i have multiple LIBOMP SH**
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
# from coqui_tts import generate_TTS_using_bark, generate_TTS_using_coqui
import shutil
from tqdm import tqdm
from faster_whisper import WhisperModel
from gtts import gTTS
from tiktok_tts_v2 import texttotiktoktts
from natsort import natsorted
from reddit_playwright import get_reddit_data
from reddit_playwright import get_reddit_title
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import asyncio

load_dotenv()
reddit_user = os.getenv("REDDIT_USER")
reddit_pw = os.getenv("REDDIT_PW")

video_files_list = []
audio_files_list = []


def delete_temp_audio(folder_path="./resources/reddit/audio"):
    # If temp folder is found, delete it
    if os.path.exists(folder_path):
        print(f"deleting {folder_path}")
        shutil.rmtree(folder_path)
        print("removed temp audio")
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

def get_reddit_title_image(url):
    
    # def login(page, url):
    #     # page = await context.new_page()
    #     page.set_viewport_size({"width": int(485), "height": 800})

    #     page.goto(url)
    #     page.locator("input[name=\"username\"]").fill(reddit_user)
    #     page.locator("input[name=\"password\"]").fill(reddit_pw)
    #     time.sleep(1)
    #     page.get_by_role("button", name="Log In").click()
    #     # page.keyboard.press('Enter')
        
    #     # let the login take place.
    #     time.sleep(15)
        
    #     # for some reason the context doesn't hold so dont close the page.
    #     # await page.close()
    
    #     return    
    
    # with sync_playwright() as p:
    #     browser = p.chromium.launch(headless=False)
    #     # browser = await p.chromium.launch()
    #     page = browser.new_page()
        
    #     # log in
    #     login(page, "https://www.reddit.com/login")
        
    #     page.set_viewport_size({"width": int(485), "height": 800})
    #     page.goto(url)
    #     time.sleep(5)
    #     # title of the page
    #     # title = page.locator("shreddit-post")
    #     title = page.get_by_test_id("post-content")
        
    #     title.screenshot(path="./resources/reddit/post.png")
    #     browser.close()
    
    asyncio.run(get_reddit_title(url))
    # create imageclip from title
    image_path = "./resources/reddit/post.png"
    image_clip = ImageClip(image_path)

    return image_clip    


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
    voice = random.randint(0, 8)
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
    # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
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



def generate_reddit_video(url, num_posts=10, num_comments=3, crop=False, useSRT=True, usePlaywright=True):
    
    def make_sentences(post, num_comments=3):
        sentences = []
        # post_author = post["author"]
        post_author = post["author"] if not any(char.isdigit() for char in post["author"]) else "Redditor"
        post_title = post["title"]
        post_body = post["selftext"]
        post_comments = post["comments"]
    
        # sentences.append(f"{post_author} said {post_title}")
        sentences.append(f"Daily Dose of Reddit: {post_title}")
        if post_body.strip() and len(post_body.split()) < 10:
            sentences.append(post_body)
    
        # Generate Textclips for the comments
        # print(f"number of comments: {len(post_comments)}")
        for i, post_comment in enumerate(post_comments):
            # comment_author = post_comment["author"]
            # comment_author = post_comment["author"] if not any(char.isdigit() for char in post_comment["author"]) else "Redditor"
            comment_body = post_comment["comment"]
            # comment_ups = post_comment["ups"]
            comment_index = post_comment["index"]
            
            word_count = len(comment_body.split())
            if word_count > 25:
                continue
            senten = f"Redditor {comment_index} said {comment_body}"
            print(senten)
            # sentences.append(f"{comment_author} said {comment_body}")
            sentences.append(f"Redditor said {comment_body}")
            # sentences.append(f"{comment_body}")
            print(len(sentences))
            if len(sentences) > num_comments:
                print(f"{len(sentences)} found. Breaking")
                break

        sentences.append("Sub, Comment, Like for More!")
        # for sent in sentences: 
        #     print(sent)
    
        return sentences
    
    size = (720, 1280)
    
    # Get each post for each post that comes back
    posts = asyncio.run(get_reddit_data(reddit_url=url, num_posts=num_posts))
    print("\n\nFinished getting all the posts! Lets begin MoviePy stuff.\n")
    # time.sleep(30) # wait artifically because reddit is catching on
    for i, post in enumerate(posts): 
        
        image_clip = None
        if(usePlaywright):
            # Generate title screenshot of reddit page
            # image_clip = get_reddit_title_image(post["url"])
            image_path = f"./resources/reddit/post-{i}.png"
            image_clip = ImageClip(image_path)
        
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
            if(usePlaywright):
                image_clip = image_clip.set_start(0).set_duration(clip_duration).resize(width=int(720*0.95)).set_position(("center", 0.1), relative=True).set_opacity(0.9)
            else:
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
            if(usePlaywright):
                final_video_clip = CompositeVideoClip([video_clip, image_clip, text_clip_body], use_bgclip=True)
            else:
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
        reddit_path = "resources\\uploaded_videos\\reddit"
        title = f"Daily Dose of AskReddit #shorts #fyp #reddit #cats #dogs #questions #thoughts {i}"
        reddit_file = os.path.join(reddit_path, f"{title}.mp4")
        # reddit_path = os.path.join("resources", "uploaded_videos", f"reddit")
        # reddit_file = os.path.join("resources", "uploaded_videos", f"reddit", f"reddit_{i}.mp4")
        # final_video.save_frame("frame.png", t=1)
        # exit()
        final_video.write_videofile(reddit_file, fps=30, threads=1, codec='h264_nvenc')
        
        # time taken?
        end_time = time.time()  
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

def main():
    
    # Setup files
    delete_temp_audio()
    audio_type = "happy" # change this to categories eventually, look up music dmca stuff
    audio_path = f"resources\\audio\\{audio_type}"
    video_path = "resources\\background_videos\\scraper\\catsdogsanimalspetsvertical\\vertical"#scraper\\verticalyoga"
    get_video_files(video_path)
    get_audio_files(audio_path)
    
    # Variables to setup - Required!
    # url = "https://www.reddit.com/r/Ask/top.json?t=day"
    url = "https://www.reddit.com/r/AskReddit/top.json?t=day"
    num_posts = 5
    num_comments = 3
    crop = False
    useSRT = True
    usePlaywright = True
    
    # Start generation
    generate_reddit_video(url, num_posts=num_posts, num_comments=num_comments, crop=crop, useSRT=useSRT,usePlaywright=usePlaywright)
    
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