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
from tts import generate_TTS_using_bark, generate_TTS_using_coqui
import shutil
from tqdm import tqdm
from faster_whisper import WhisperModel
from gtts import gTTS
from tiktok_tts_v2 import texttotiktoktts


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

def generate_TTS_using_TikTok(sentences):
    def delete_temp_audio(folder_path="resources\\temp\\audio"):
        # If temp folder is found, delete it
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        # Create the folder
        os.mkdir(folder_path)
        
        return
    
    # delete_temp_audio()
    
    path = os.getcwd() + "\\resources\\temp\\audio"
    tts_files = []
    success = False
    for i, sentence in enumerate(sentences):
        
        success, tts_file = texttotiktoktts(sentence, "en_us_001", path, file_name=f"audio_tts_{i}")
        tts_files.append(tts_file)
        # print(tts_file)
    
    if not success: exit()
    return tts_files

def generate_srt_from_audio_using_whisper(audio_file_path):
    
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

def add_text_clip(text="", font_name="Impact", font_size=30, font_color="white", bg_color="black", size=(int(720*0.9),None), method="label", start=0, total_duration=5, opacity=1.0, position_y=0.5):
    text_clip = TextClip(text, fontsize=font_size, color=font_color, bg_color=bg_color, font=font_name, size=size, method=method)
    text_clip = text_clip.set_position(("center",position_y), relative=True).set_start(start).set_duration(total_duration).set_opacity(opacity)
    return text_clip

def add_video_clip(path, start=0, total_duration=5, size=(720,1280)):
    video_file = get_video_file(path)
    video_clip = VideoFileClip(video_file, audio=True).loop(total_duration)
    video_clip = video_clip.set_start(start).set_duration(total_duration).resize(size)
    return video_clip

def add_audio_tts_clip(audio_file, silence=1, start=0):
    # print(audio_file)
    audio_clip = AudioFileClip(audio_file)
    clip_duration = audio_clip.duration + silence
    audio_clip = audio_clip.set_start(start)
    
    return audio_clip, clip_duration

def create_video_audio_text_clip(text, text_options={}, video_options={}, audio_options={}):

    print('generating video...')
    tts_file = generate_TTS_using_TikTok([text])
    tts_clip, clip_duration = add_audio_tts_clip(tts_file[0])
    text_clip = add_text_clip(text=text, total_duration=clip_duration)
    video_clip = add_video_clip(path="jokes", total_duration=clip_duration)
    final_video = CompositeVideoClip([video_clip, text_clip], use_bgclip=True)
    final_video = final_video.set_audio(tts_clip)
    # filename = "test.mp4"
    # final_video.write_videofile(filename, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
    # final_video.write_videofile(filename, fps=30, preset='ultrafast')
    # exit()
    return final_video

# def create_final_video(video_clips):
    
#     return final_video

def main():
    texts = [    "Once upon a time, in a charming little town,",    
             "Lived a cat named Oliver, with fur of golden brown.",    
             "And nearby, a dog named Max, full of playful zest,",    
             "With a wagging tail and a heart so blessed.",    
             "Oliver would perch on a windowsill high,",    
             "Watching the world with a curious eye.",    
             "Max would bound and chase his tail around,",    
             "With a barking joy, a joyful sound.",    
             "They met one day under a bright blue sky,",    
             "A cat and a dog, unlikely allies.",    
             "They played and explored, side by side,",    
             "Creating memories, their friendship amplified.",    
             "Through fields they roamed, a duo so true,",    
             "Sharing adventures, just Max and Oliver knew.",    
             "With every passing day, their bond grew strong,",    
             "A cat and a dog, proving friendships can't go wrong."]

    # generate the video including the sentence, and tts
    video_clips = []
    for text in texts: 
        video = create_video_audio_text_clip(text)
        video_clips.append(video)
    final_video = concatenate_videoclips(video_clips)
    
    # Set the background audio music
    audio_path = get_audio_file("happy")
    background_audio_clip = AudioFileClip(audio_path).set_duration(final_video.duration)
    background_audio_clip = background_audio_clip.volumex(0.1) # set volume of background_audio to 10%
    combined_audio = CompositeAudioClip([background_audio_clip, final_video.audio])
    
    final_video = final_video.set_audio(combined_audio)
    final_video.write_videofile("story.mp4", fps=30, preset='ultrafast')

    return

if __name__ == "__main__":
    main()