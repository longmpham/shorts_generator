import requests
import json
import base64
import re
import os
from tqdm import tqdm
import time

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

def texttotiktoktts(text="", voice="en_us_001", path="", file_name="tts_audio.mp3"):
    # if i call this too fast, it fails. 
    while(True):    
        try:
            response = requests.post('https://tiktok-tts.weilnet.workers.dev/api/generation',
                                    json={"text": text, "voice": voice})
            jsondata = json.loads(response.text)
            error = jsondata.get("error")

            if error is None:
                audio_base64 = jsondata["data"]
                text = re.sub(r"[^a-zA-Z0-9]+", "", text)[:61]  # Filter and limit export name

                audio_data = base64.b64decode(audio_base64)

                if not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)

                file_path = os.path.join(path, f"{file_name}.mp3")

                # simple with no tqdm 
                # with open(file_path, "wb") as file:
                    # file.write(audio_data)
                
                # with tqdm
                with open(file_path, "wb") as file:
                    total_size = len(audio_data)
                    chunk_size = 4096

                    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Writing audio") as progress_bar:
                        bytes_written = 0

                        while bytes_written < total_size:
                            chunk = audio_data[bytes_written:bytes_written + chunk_size]
                            file.write(chunk)
                            bytes_written += len(chunk)
                            progress_bar.update(len(chunk))

                return True, file_path
            else:
                print(f"Error: {error}")
                return False, error
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(1)
            # return False, "An error has occurred"
