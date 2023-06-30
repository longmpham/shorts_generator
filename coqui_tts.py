from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from pydub import AudioSegment
import nltk  # we'll use this to split into sentences
import numpy as np
from bark.generation import (
    preload_models,
    load_codec_model,
)
from moviepy.editor import *
import torch
import torchaudio
from TTS.api import TTS

model = load_codec_model(use_gpu=True)
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

coqui_speaker_list = [
    "tts_models/en/jenny/jenny", # OK
    "tts_models/en/ljspeech/tacotron2-DCA", #BAD
    "tts_models/en/ljspeech/glow-tts", #BAD
    "tts_models/en/ljspeech/tacotron2-DDC", #BAD
    "tts_models/en/ljspeech/fast_pitch", #OK
    "tts_models/en/multi-dataset/tortoise-v2", #OK but long time and different results
    "tts_models/uk/mai/glow-tts", # BAD
    "tts_models/uk/mai/vits", # BAD
    "tts_models/en/blizzard2013/capacitron-t2-c150_v2", # doesnt work
    "tts_models/en/sam/tacotron-DDC", # doesn't work
    "tts_models/en/ljspeech/neural_hmm", # doesn't work
    "tts_models/en/ljspeech/fast_pitch", # OK
    "tts_models/en/ljspeech/overflow", # doesn't work
]


def generate_TTS_using_bark(text_prompt):
    
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
        audio_array = generate_audio(text, history_prompt=speaker_list[3], text_temp=0.9, waveform_temp=0.9)
        pieces += [audio_array, silence.copy()]
        write_wav(f"output_{i}.wav", SAMPLE_RATE, audio_array)
        audio_files.append(f"output_{i}.wav")
    
    # combine audio clips
    audio1 = AudioFileClip(audio_files[0])
    audio2 = AudioFileClip(audio_files[1])
    # audio1 = audio1.set_duration(7)
    # audio2 = audio2.set_duration(3)
    
    # # Concatenate all the audio clips together.
    # combined_audio = concatenate_audioclips([audio1, audio2])

    # # create the wav file
    # combined_audio_path = "combined_audio.mp3"
    # combined_audio.write_audiofile(combined_audio_path)
    
    
    # return combined_audio_path
    return [audio1,audio2]

def generate_TTS_using_coqui(text_prompts):
    # In terminal type below to get list of speaker names.
    # tts --list_models

    # Init TTS
    tts = TTS(model_name=coqui_speaker_list[0], progress_bar=True, gpu=False)
    # Run TTS
    # ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
    # Text to speech with a numpy output
    # wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
    # Text to speech to a file
    tts_files = []
    for i, text in enumerate(text_prompts):
        file_name = f"output_{i+1}.wav"
        tts.tts_to_file(text=text, file_path=file_name)
        tts_files.append(file_name)

    return tts_files

# generate_TTS_using_bark(["hello world","how are you"])

# generate_TTS_using_coqui(["What do you call a bear with no teeth?", "A gummy bear"])








#  1: tts_models/multilingual/multi-dataset/your_tts [already downloaded]
#  7: tts_models/en/ek1/tacotron2 [already downloaded]
#  8: tts_models/en/ljspeech/tacotron2-DDC
#  9: tts_models/en/ljspeech/tacotron2-DDC_ph
#  10: tts_models/en/ljspeech/glow-tts [already downloaded]
#  11: tts_models/en/ljspeech/speedy-speech [already downloaded]
#  12: tts_models/en/ljspeech/tacotron2-DCA
#  13: tts_models/en/ljspeech/vits
#  14: tts_models/en/ljspeech/vits--neon
#  15: tts_models/en/ljspeech/fast_pitch
#  16: tts_models/en/ljspeech/overflow
#  17: tts_models/en/ljspeech/neural_hmm [already downloaded]
#  18: tts_models/en/vctk/vits
#  19: tts_models/en/vctk/fast_pitch
#  20: tts_models/en/sam/tacotron-DDC
#  21: tts_models/en/blizzard2013/capacitron-t2-c50
#  22: tts_models/en/blizzard2013/capacitron-t2-c150_v2
#  23: tts_models/en/multi-dataset/tortoise-v2
#  24: tts_models/en/jenny/jenny [already downloaded]
#  29: tts_models/uk/mai/glow-tts
#  30: tts_models/uk/mai/vits
#  Name format: type/language/dataset/model
#  1: vocoder_models/universal/libri-tts/wavegrad
#  2: vocoder_models/universal/libri-tts/fullband-melgan
#  3: vocoder_models/en/ek1/wavegrad [already downloaded]
#  4: vocoder_models/en/ljspeech/multiband-melgan [already downloaded]
#  5: vocoder_models/en/ljspeech/hifigan_v2 [already downloaded]
#  6: vocoder_models/en/ljspeech/univnet
#  7: vocoder_models/en/blizzard2013/hifigan_v2
#  8: vocoder_models/en/vctk/hifigan_v2
#  9: vocoder_models/en/sam/hifigan_v2
#  10: vocoder_models/nl/mai/parallel-wavegan
#  11: vocoder_models/de/thorsten/wavegrad
#  12: vocoder_models/de/thorsten/fullband-melgan
#  13: vocoder_models/de/thorsten/hifigan_v1
#  14: vocoder_models/ja/kokoro/hifigan_v1
#  15: vocoder_models/uk/mai/multiband-melgan
#  16: vocoder_models/tr/common-voice/hifigan