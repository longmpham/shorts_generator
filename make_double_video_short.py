from moviepy.editor import *
from moviepy.video.fx.all import *


def generate_final_video(top_video_path, bottom_video_path, top_text, bottom_text, final_video_path):
    size = (1280, 720)

    top_video_clip = VideoFileClip(top_video_path, audio=False)
    # bottom_video_clip = VideoFileClip(bottom_video_path, audio=False).loop(10)
    bottom_video_clip = VideoFileClip(bottom_video_path, audio=False)
    top_black_bar = ImageClip("resources\\black_image.png").set_duration(top_video_clip.duration).set_position(("center","top")).resize(size)
    bottom_black_bar = ImageClip("resources\\black_image.png").set_duration(top_video_clip.duration).set_position(("center","bottom")).resize(size)

    top_text_clip = TextClip(top_text, size=(720, 100), color="white").set_position(("center", "center")).set_duration(10)
    bottom_text_clip = TextClip(bottom_text, size=(720, 100), color="white").set_position(("center", "center")).set_duration(10)

    final_top_video_text_clip = CompositeVideoClip([top_black_bar, top_text_clip])
    final_top_video_text_clip = final_top_video_text_clip.set_duration(10)
    final_bottom_video_text_clip = CompositeVideoClip([bottom_black_bar, bottom_text_clip])
    final_bottom_video_text_clip = final_bottom_video_text_clip.set_duration(10)

    combine = clips_array([[final_top_video_text_clip], [top_video_clip], [bottom_video_clip], [final_bottom_video_text_clip]])
    
    # Set Audio
    # combine = combine.set_audio().set_duration(10)
    # combine.save_frame("frame.png", t=1)
    combine.write_videofile(final_video_path)

    combine.close()

top_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\resources\\background_videos\\genshin\\Genshin Impact 2023.06.23 - 17.58.53.28.DVR.mp4"
bottom_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\resources\\background_videos\\genshin\\Genshin Impact 2023.06.23 - 18.00.41.33.DVR.mp4"
final_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\final_video_test.mp4"
top_text = "Top Text Clip"
bottom_text = "Bottom Text Clip"

generate_final_video(top_video_path, bottom_video_path, top_text, bottom_text, final_video_path)



















# top_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\resources\\background_videos\\genshin\\Genshin Impact 2023.06.23 - 17.58.53.28.DVR.mp4"
# bottom_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\resources\\background_videos\\genshin\\Genshin Impact 2023.06.23 - 18.00.41.33.DVR.mp4"
# final_video_path = "C:\\Users\\longp\\Documents\\Coding\\shorts_generator\\final_video_test.mp4"

# # size=(720,1280)
# size=(1280,720)
# # top_video_clip = VideoFileClip(top_video_path).fx(afx.audio_normalize).resize(size)
# top_video_clip = VideoFileClip(top_video_path, audio=False)
# bottom_video_clip = VideoFileClip(bottom_video_path, audio=False).loop(10)
# top_black_bar = ImageClip("resources\\black_image.png").set_duration(top_video_clip.duration).set_position(("center","top")).resize(size)
# bottom_black_bar = ImageClip("resources\\black_image.png").set_duration(top_video_clip.duration).set_position(("center","bottom")).resize(size)


# # top_video_clip = top_video_clip.crop(x1=640, y1 = 0, x2=1280, y2 = 360)
# top_text_clip = TextClip("Top Text Clip", size=(720,100), color="white").set_position(("center","center")).set_duration(10)
# bottom_text_clip = TextClip("Bottom Text Clip", size=(720,100), color="white").set_position(("center","center")).set_duration(10)

# #text3 = TextClip("la produccion de GH", size=(720,100), color="white").set_position(("center",text.h+135)).set_duration(10)
# width,height = top_video_clip.size

# final_top_video_text_clip = CompositeVideoClip([top_black_bar, top_text_clip])

# final_bottom_video_text_clip = CompositeVideoClip([bottom_black_bar, bottom_text_clip])

# combine = clips_array([[final_top_video_text_clip],[top_video_clip],[bottom_video_clip],[final_bottom_video_text_clip]])

# combine.save_frame("frame.png", t = 1)

# # combine.write_videofile(final_video_path)

# combine.close()