import os
import subprocess
from multiprocessing import Pool

def transcode_to_srt(input_file, output_file, subtitle_delay):
    subprocess.call(['ffmpeg', '-itsoffset', subtitle_delay, '-i', input_file, '-map', '0:s:0?', output_file])

def transcode_file(file_info):
    input_file, output_file, subtitle_delay = file_info
    transcode_to_srt(input_file, output_file, subtitle_delay)

def transcode_folder_to_srt(folder_path, delay, use_multiprocessing=False):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.mp4', '.mkv')):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, os.path.splitext(file)[0] + '.srt')
                file_list.append((input_file, output_file, delay))
    print(file_list)
    if use_multiprocessing:
        with Pool() as pool:
            pool.map(transcode_file, file_list)
    else:
        for file_info in file_list:
            transcode_file(file_info)

def convert_m4v_to_mp4(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.m4v'):
                input_file = os.path.join(root, file)
                print(input_file)
                output_file = os.path.join(root, os.path.splitext(file)[0] + '.mp4')
                convert_command = ['ffmpeg', '-i', input_file, '-c:v', 'copy', '-c:a', 'copy', output_file]
                subprocess.call(convert_command)

# Usage example
folder_path = "Z:\\data\\media\\tvshows\\South Park (1997)\\Season 10"
convert_m4v_to_mp4(folder_path)
# delay = '5'
delay = '0'
use_multiprocessing = False

transcode_folder_to_srt(folder_path, delay, use_multiprocessing)
# file = "Z:\\data\\media\\tvshows\\South Park (1997)\\Season 7\\South Park - S07E15 - It's Christmas in Canada HDTV-1080p.mp4"
# transcode_to_srt(file, "srt.srt", "0")
