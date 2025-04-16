# Shorts Generator

Reused some information from AITA project and created a lot of shorts for youtube shorts. Making it as general as possible so that I can just pull data and upload!

Prerequisite:
Working with Python 3.10.11
Imagick is required too. install with the legacy option selected.
Works with ImageMagick-7.1.1-10-Q16-HDRI-x64-dll.exe 


How to use:
1. Get the git repo in a local directory
2. Activate a Python Env by typing in `python -m venv venv` (the dot refers to the current directory!, or call it a name. ie. venv)
3. Activate the Python Env by typing `.\venv\Scripts\activate` in the terminal.
4. Using the requirements.txt, install the necessary packages required (comes from `pip freeze > requirements.txt`)
`pip install -r requirements.txt`. This should install all the necessary packages required. The GPU is NVIDIA based and contains the packages in the requirements.txt as well. If it helps I used this link: https://github.com/SYSTRAN/faster-whisper/issues/1080. Installing faster_whisper should work at this point. If not, go to the pypi for faster_whisper and checkout the installation instructions https://pypi.org/project/faster-whisper/
5. You may have to install playwright. Run the `python playwright install` to install playwright in your environment.
6. Follow the directory I have layed out or change them to your liking... you'll need your own audio/video files to make the clips!
6. Recommended to create your own .env file to make logins for reddit.

<todo: fix pathing up...>
/resources
  /audio/<topic>/
  /background_videos/<topic>/
  /data
  /screenshots
  /temp
  /tiktok
  /uploaded_videos

Notes:
In moviepy (moviepy==2.1.2) ffmpeg_reader.py, I commented out the `print(self.infos)` line for cleaner logs and `print(" ".join(cmd))`. It was driving me crazy.

Helpful links:
https://developer.nvidia.com/cuda-downloads
https://developer.nvidia.com/cudnn-downloads
https://github.com/SYSTRAN/faster-whisper/issues/1080
https://pypi.org/project/faster-whisper/


Todos:
- clean up function and process
- remove old stuff