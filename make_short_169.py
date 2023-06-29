import shutil
import datetime
import random
from moviepy import *
from moviepy.editor import *
from moviepy.video.fx.all import *
from tiktok_tts_v2 import texttotiktoktts
from skimage.filters import gaussian
# from pydub import AudioSegment
from datetime import timedelta
# from tqdm import tqdm
from faster_whisper import WhisperModel
from moviepy.video.tools.subtitles import SubtitlesClip

counter = 0
size = (1280, 720)

def get_todays_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d")
    return formatted_date

def delete_temp_audio(folder_path="resources\\temp\\audio"):
    # If temp folder is found, delete it
    if os.path.exists(folder_path):
        print(f"deleting {folder_path}")
        shutil.rmtree(folder_path)
        print("removed")
    # Create the folder
    os.makedirs(folder_path)
    return

def get_video_file(goal_name):
    background_video_dir = os.path.join(os.getcwd(), "resources", "background_videos", f"{goal_name}")
    background_video_files = [f for f in os.listdir(background_video_dir) if f.endswith(".mp4")]
    background_video_file = os.path.join(background_video_dir, random.choice(background_video_files))
    return background_video_file

def get_audio_file(audio_type):
    background_audio_dir = os.path.join(os.getcwd(), "resources", "audio", f"{audio_type}")
    background_audio_files  = [f for f in os.listdir(background_audio_dir) if f.endswith(".mp3")]
    background_audio_file = os.path.join(background_audio_dir, random.choice(background_audio_files))
    return background_audio_file

def generate_TTS_using_TikTok(sentence):

    global counter
    voices = [
        "en_us_001", # Female
        "en_us_006", # Male 1 # sucks
        "en_us_007", # Male 2 # better
        "en_us_009", # Male 3
        "en_us_010", # Male 4 # best
        "en_uk_001",
        "en_uk_003",
    ]
        
    path = os.getcwd() + "\\resources\\temp\\audio"
    success, tts_file = texttotiktoktts(sentence, voices[6], path, file_name=f"tts_audio_file_{counter}")
    counter += 1
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
    
    # use large-v2 model and transcribe the audio file
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")
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
            print("using per word")
            for segment in segments:
                words = ""
                for index, word in enumerate(segment.words):
                    print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
                    srt_file.write(f"{index}\n")
                    # srt_file.write(f"{word.start:.2f} --> {word.end:.2f}\n")
                    srt_file.write(f"{format_timedelta(word.start)} --> {format_timedelta(word.end)}\n")
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
    
    return srt_file_path

def add_text_clip(text="", font_name="Impact", font_size=50, font_color="white", bg_color="black", size=(int(720*0.9),None), method="caption", start=0, total_duration=5, opacity=1.0, position=("center"), relative=False):
    text_clip = TextClip(text, fontsize=font_size, color=font_color, bg_color=bg_color, font=font_name, size=size, method=method)
    if relative==True:
        text_clip = text_clip.set_position(position, relative=True).set_start(start).set_duration(total_duration).set_opacity(opacity)
    else:   
        text_clip = text_clip.set_position(position).set_start(start).set_duration(total_duration).set_opacity(opacity)
    return text_clip

def add_video_clip(category, start=0, total_duration=5, size=(720,1280)):
    blur_image = False
    
    video_file = get_video_file(category)
    video_clip = VideoFileClip(video_file, audio=True).loop(total_duration)
    video_clip = video_clip.set_start(start).set_duration(total_duration).resize(size)
    # video_clip = video_clip.set_start(start).set_duration(total_duration).resize(height=size[1]).crop(x1=780, width=720, height=1280)
#     resize(height=1920)
#       crop(x_center=960, y_center=960, width=1080, height=1920)
    
    
    def blur(image, blur_level=5):
        """ Returns a blurred (blur_level=radius=3 pixels) version of the image """
        return gaussian(image.astype(float), sigma=blur_level)
    
    if blur_image == True:
        print(f'blurring image because blur is {blur_image}')
        # video_clip = video_clip.fl_image(blur)
        video_clip = video_clip.fl_image(lambda image: blur(image, blur_level=5))
    return video_clip

def add_background_audio(final_video, audio_type):
    
    audio_path = get_audio_file(audio_type)
    background_audio_clip = AudioFileClip(audio_path)
    background_audio_clip = background_audio_clip.volumex(0.1) # set volume of background_audio to 10%
    combined_audio = CompositeAudioClip([background_audio_clip, final_video.audio])
    combined_audio = afx.audio_loop(combined_audio, duration=final_video.duration)
    final_video = final_video.set_audio(combined_audio)
    
    return final_video

def add_audio_tts_clip(audio_file, silence=2, start=0):
    # print(audio_file)
    audio_clip = AudioFileClip(audio_file)
    clip_duration = audio_clip.duration + silence
    audio_clip = audio_clip.set_start(start)
    
    return audio_clip, clip_duration

def generate_169_video(top_text, bottom_text, video_category="jokes"):

    useSRT = True
    # generate tts
    tts_file = generate_TTS_using_TikTok(bottom_text)
    print("TTS generated!")
    tts_clip, clip_duration = add_audio_tts_clip(tts_file)
    print("TTS clips done!")
    
    
    # generate text
    top_text_clip = add_text_clip(text=top_text, font_size=100, position=("center", "center"), total_duration=clip_duration)
    bottom_text_clip = add_text_clip(text=bottom_text, position=("center", "top"), total_duration=clip_duration)
    
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
    video_clip = add_video_clip(video_category, start=0, total_duration=clip_duration, size=size)

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

    # combined_video.close()
    return combined_video
    
def main():
    audio_type = "happy"
    video_category = "genshin"
    final_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\final_video_169.mp4"
    title = f"Genshin Impact Facts"
    texts = [
        "Did you know about these facts about Kazuha?",
        "He loves to write poetry, specifically Haikus",
        "He had a wealthy family met with a tragic fate",
        "He loves to sit by the rain and listen to the sounds of them falling",
        "He plays a flute that ties together his love for poetry",
        "Sub, Comment, Like for More!"
    ]

    # generate the clips and put them together. 
    # these clips contain tts, text, and the video.
    video_clips = []
    for text in texts:
        print("generating video clip...")
        video_clip = generate_169_video(title, text, video_category)
        video_clips.append(video_clip)
    final_video = concatenate_videoclips(video_clips)

    # Set the final background audio music
    final_video = add_background_audio(final_video, audio_type)
    
    # Write the final video
    # final_video.save_frame("frame.png", t=1)
    final_video.write_videofile(final_video_path, fps=30, preset='ultrafast')
  
    return

if __name__ == "__main__":
    main()
    
# +------------+
# |            |
# |   Title    |
# |            |
# +------------+
# |            |
# |   Video    |
# |            |
# +------------+
# |    Text    |
# |            |
# |            |
# +------------+
