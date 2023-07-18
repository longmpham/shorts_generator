from TikTokAPI import TikTokAPI
import json


# https://github.com/avilash/TikTokAPI-Python

# Save my cookies to a cookies_file_path
def read_json_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if type(data) is str:
        return json.loads(data)
    return data

# Go to Chrome and grab your cookies (F12, Application, Cookies) and save it in cookies.json
api = TikTokAPI(read_json_from_file("cookies.json"))


# api = TikTokAPI(cookie=cookie)
number_of_videos = 30
# data = api.getTrending(count=number_of_videos)  # currently only returns ticktok trash 5 videos
data = api.getVideosByHashTag("funny", count=number_of_videos)
print(data)

# for i in range(number_of_videos):
#     video_id = data['items'][i]['video']['id']
#     print(video_id)
    
#     save_path = f"resources\\tiktok\\{video_id}.mp4"
#     api.downloadVideoById(video_id=video_id, save_path=save_path)