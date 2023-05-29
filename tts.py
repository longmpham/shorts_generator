from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from pydub import AudioSegment
import nltk  # we'll use this to split into sentences
import numpy as np
from bark.generation import (
    preload_models,
)
from moviepy.editor import *

SUNO_USE_SMALL_MODELS=True # uses 8GB VRAM instead of 12GB recommended

# English Prompt names
speaker_list = [
    'v2/en_speaker_0',
    'v2/en_speaker_1',
    'v2/en_speaker_2',
    'v2/en_speaker_3', # EU GUY
    'v2/en_speaker_4',
    'v2/en_speaker_5', # Grainy
    'v2/en_speaker_6', # Suno Favourite
    'v2/en_speaker_7',
    'v2/en_speaker_8',
    'v2/en_speaker_9'
]


def generate_TTS_using_bark(text_prompt):
    # download and load all models
    preload_models()

    # generate audio from text
    # format should be 2 csv fields so expect a dict of strings. ie. ["what is the ...", "that thing!"]
    text_prompts = text_prompt if text_prompt else "Do you know this one?"

    # split to sentences using nltk
    # sentences = nltk.sent_tokenize(text_prompt)

    # generate audio for each sentence
    silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
    pieces = []
    audio_files = []
    # for i, sentence in enumerate(sentences):
    for i, text in enumerate(text_prompts):
        audio_array = generate_audio(text, history_prompt=speaker_list[3])
        pieces += [audio_array, silence.copy()]
        wav_file = write_wav(f"output_{i}.wav", SAMPLE_RATE, audio_array)
        audio_files.append(wav_file)
    wav_file = write_wav(f"final_output.wav", SAMPLE_RATE, pieces)

    
    # combine audio clips
    audio1 = AudioSegment.from_file(audio_files[0])
    audio2 = AudioSegment.from_file(audio_files[1])
    
    # Calculate the duration difference for each clip
    duration_difference_clip1 = 7000 - audio1.duration * 1000  # Difference in milliseconds
    duration_difference_clip2 = 3000 - audio2.duration * 1000  # Difference in milliseconds
    
    # Extend the audio clips by the duration differences
    extended_clip1 = audio1.fx('loop', n=(duration_difference_clip1 // audio1.duration) + 1)
    extended_clip2 = audio2.fx('loop', n=(duration_difference_clip2 // audio2.duration) + 1)
    
    
    combined_audio = concatenate_audioclips([extended_clip1, extended_clip2])

    # create the wav file
    combined_audio_path = "combined_audio.mp3"
    combined_audio.write_audiofile(filename=combined_audio_path, fps=extended_clip1.fps, verbose=True, write_logfile=True)
    
    
    # return combined_audio_path
    return


generate_TTS_using_bark(["hello world","how are you"])






# [laughter]
# [laughs]
# [sighs]
# [music]
# [gasps]
# [clears throat]
# — or ... for hesitations
# ♪ for song lyrics
# CAPITALIZATION for emphasis of a word
# [MAN] and [WOMAN] to bias Bark toward male and female speakers, respectively
