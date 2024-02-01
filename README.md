# Shorts Generator

Reused some information from AITA project and created a lot of shorts for youtube shorts. Making it as general as possible so that I can just pull data and upload!

Prerequisite:
Working with Python 3.10.11
Imagick is required too. install with the legacy option selected.
Works with ImageMagick-7.1.1-10-Q16-HDRI-x64-dll.exe 


How to use:
1. Get the git repo in a local directory
2. Activate a Python Env by typing in `python -m venv .` (the dot refers to the current directory!)
3. Activate the Python Env by typing `.\Scripts\activate` in the terminal.
4. Using the requirements.txt, install the necessary packages required (comes from `pip freeze > requirements.txt`)
`pip install -r requirements.txt`
5. Torch may not install correctly, if so, try this:
`pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
note: this is only if you want to transcribe with CUDA capable devices, otherwise you can just use your CPU instead (longer times to transcribe audio)
6. Follow the directory I have layed out or change them to your liking... you'll need your own audio/video files to make the clips!


<todo: fix pathing up...>
/resources
  /audio/<topic>/
  /background_videos/<topic>/
  /data
  /screenshots
  /temp
  /tiktok
  /uploaded_videos

