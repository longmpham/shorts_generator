from moviepy.editor import CompositeVideoClip, ImageClip
from moviepy.video.fx import resize
from moviepy.video.VideoClip import TextClip


def generate_thumbnail(title, logo_path, background_path):
    # Create image clips from the inputs
    title_clip = TextClip(title, fontsize=50, color='white', font='Arial-Bold', stroke_color='black', stroke_width=1, size=(1280*0.25, None), method="caption")
    logo_clip = ImageClip(logo_path)
    background_clip = ImageClip(background_path).resize((1280, 720))

    # Resize the clips to 1280x720
    title_clip = title_clip.resize((1280*0.55, 720*0.8))
    logo_clip = logo_clip.resize((600, 450))
    background_clip = background_clip.resize((1280, 720))
    
    # Set the position and duration of the title and logo clips
    title_clip = title_clip.set_position((-0.05, 0), relative=True)
    logo_clip = logo_clip.set_position((0.5, 0.4), relative=True)
        
    
    # Rotate the title clip by 10 degrees
    title_clip = title_clip.rotate(10, unit="deg", expand=True)
    
    # Concatenate the clips together
    composite_clip = CompositeVideoClip([background_clip, logo_clip, title_clip], use_bgclip=True)

    # Export the final thumbnail as a video file
    # composite_clip.write_videofile("thumbnail.mp4", fps=30, preset='ultrafast')
    composite_clip.save_frame("thumbnail.png", t=1)

background_image = "resources\\background_videos\\diablo4\\images\\d4_image1.png"
logo = "resources\\background_videos\\diablo4\\images\\d4logo.png"
title = "GREAT NEWS COMING"
generate_thumbnail(title, logo, background_image)