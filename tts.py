from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from IPython.display import Audio
import nltk  # we'll use this to split into sentences
import numpy as np
from bark.generation import (
    preload_models,
)

# English Prompt names
speaker_list = [
    'v2/en_speaker_0',
    'v2/en_speaker_1',
    'v2/en_speaker_2',
    'v2/en_speaker_3',
    'v2/en_speaker_4',
    'v2/en_speaker_5', # Grainy
    'v2/en_speaker_6', # Suno Favourite
    'v2/en_speaker_7',
    'v2/en_speaker_8',
    'v2/en_speaker_9'
]

# download and load all models
preload_models()

# generate audio from text
# text_prompt = "So my (f16) name is Andi just Andi. \
#     My moms dad passed away just a few days before \
#     she found out she was pregnant. My mom was very \
#     close with her Dad and his name was Andrew \
#     (also went by Andy). The technical female Version \
#     of Andrew is Andrea but neither my mom nor dad \
#     liked the name but my mom wanted to honor her dad \
#     in some way so I got named Andi. Which I love my name \
#     I think it fits me. My parents got divorced when I was \
#     8 and I live with my mom most of the time but visit my \
#     dad every other weekend (as well as holidays). \
#     3 years ago my dad started dating his now fiance Kate. \
#     Kate for some reason when we met assumed my name was \
#     Andrea. I explained to her it was just Andi. She kept \
#     calling me Andrea though. I ended up telling my mom about \
#     it and she told me just to ignore Kate until she calls me \
#     Andi. Well, this past weekend I was at my dads and we were \
#     visiting some of Kates family. Well, she kept calling over \
#     for Andrea and of course, I ignored her. She got mad and said \
#     why am I ignoring her and I said because that's not my name \
#     and you know this. Her dad and brother basically laughed \
#     saying they thought I just went by Andi as a nickname and \
#     I said no it's just Andi. They then asked Kate why has she \
#     been calling me Andrea then. Well, Kate later got made calling \
#     me a brat for embarrassing her. She went on to say I knew who \
#     she was talking about and that I should have just gone with it \
#     but I was being an AH. I honestly kind of feel like in that instance \
#     I should have just answered to Andrea but I don't know. Am I The A-Hole?"
text_prompt = "So my (f16) name is Andi just Andi. \
    My moms dad passed away just a few days before \
    she found out she was pregnant. My mom was very \
    close with her Dad and his name was Andrew \
    (also went by Andy)."

# split to sentences using nltk
sentences = nltk.sent_tokenize(text_prompt)

# generate audio for each sentence
silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence
pieces = []
for i, sentence in enumerate(sentences):
    audio_array = generate_audio(sentence, history_prompt=speaker_list[6])
    pieces += [audio_array, silence.copy()]
    write_wav(f"output_{i}.wav", SAMPLE_RATE, audio_array)


Audio(np.concatenate(pieces), rate=SAMPLE_RATE)

# audio_array = generate_audio(text_prompt, speaker_list[6])

# save audio to disk
# write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
# Audio(audio_array, rate=SAMPLE_RATE)












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
