import numpy as np
import requests
import time
import json
import re
import unicodedata

from datetime import timedelta
from datetime import datetime as dt

def utc_to_relative_time(utc_timestamp):
    
    now = dt.utcnow()
    post_time = dt.utcfromtimestamp(utc_timestamp)
    # now = datetime.datetime.now()
    # post_time = datetime.datetime.fromtimestamp(utc_timestamp)
    
    time_diff = now - post_time
    if time_diff < timedelta(minutes=1):
        return 'just now'
    elif time_diff < timedelta(hours=1):
        minutes = int(time_diff.total_seconds() / 60)
        return f'{minutes} minutes ago'
    elif time_diff < timedelta(days=1):
        hours = int(time_diff.total_seconds() / 3600)
        return f'{hours} hours ago'
    else:
        days = time_diff.days
        return f'{days} days ago'

def save_json(post, file_name):
    with open(file_name, "w") as outfile:
        # Write the JSON data to the file with indentation for readability
        json.dump(post, outfile, indent=4)

def clean_json_file(input_file, output_file):
    def clean_text(text):
        # Convert to string if input is not already a string
        if not isinstance(text, str):
            text = str(text)

        # Remove Unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

        # Remove newlines ("\n")
        text = re.sub(r"\n+", " ", text)
        
        # Remove Unicode characters
        # text = re.sub(r"\\u\d{4}", "", text)
        
        # Remove other escape characters
        text = re.sub(r"\\[^\w\s]", "", text)
        
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        
        # Decode unicode to text
        text = bytes(text, 'utf-8').decode('unicode_escape')
        
        return text.strip()
    
    def clean_dictionary_values(dictionary):
        cleaned_dictionary = {}
        for key, value in dictionary.items():
            if isinstance(value, str):
                cleaned_value = re.sub(r'\\[nrt]', '', value)  # Remove escape characters (\n, \r, \t)
                cleaned_value = re.sub(r'\s+', ' ', cleaned_value)  # Remove extra white spaces
                cleaned_value = cleaned_value.strip()  # Remove leading/trailing white spaces
                cleaned_value = clean_text(value)
                cleaned_dictionary[key] = cleaned_value
            else:
                cleaned_dictionary[key] = value
        return cleaned_dictionary

    data = load_json_file(input_file)
    cleaned_data = clean_dictionary_values(data)
    save_json(cleaned_data, output_file)

def load_json_file(file_path):
    data = {}
    with open(file_path) as file:
        data = json.load(file)
    # print(data)
    return data

def get_posts(base_url):

    # get all posts from the url given
    response = requests.get(base_url, headers={"User-agent": "Mozilla/5.0"})
    data = response.json()

    # create a list of dictionaries (reddit posts) from the data
    posts = []
    for post in data["data"]["children"]:
        # if NSFW, go next
        # print(post["data"]["over_18"])
        if post["data"]["over_18"] == True: 
            continue
        
        title = post["data"]["title"]
        selftext = post["data"]["selftext"]
        author = post["data"]["author"]
        ups = str(post["data"]["ups"])
        utc_timestamp = post["data"]["created_utc"]
        url = post["data"]['url']
        utc_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(utc_timestamp))
        posts.append({
            "title": title,
            "selftext": selftext,
            "author": author,
            "ups": ups,
            "utc_timestamp": utc_timestamp,
            "relative_time": utc_to_relative_time(utc_timestamp),
            "url": url,
            "date_time": utc_time,
        })
        print(f"Getting posts from {url}...")
    print(f"finished getting posts from {base_url}")
    return posts

def get_comments(url, max_num_of_comments=30):
    url = url + ".json"
    print(f"Geting comments from {url}...")
    # get the url data from the url given
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()
    comments_data = data[1]['data']['children']
    # Sort comments_data by largest "ups"
    # comments_data.sort(key=lambda comment: comment["data"].get("ups",1), reverse=True)
    
    # Print the sorted comments
    # for i, comment in enumerate(comments_data):
    #     ups = comment["data"].get("ups",1)
    #     print(f"{i} - Ups: {ups}")
    # exit()
    
    # get the post body data from data
    comments = []
    for index, comment in enumerate(comments_data):
        if "author" not in comment["data"]:
            print(f"No more comments to add. Comments found: {index}")
            break
        # Skip comment if more than 30 words
        comment_body = comment["data"]["body"]
        word_count = len(comment_body.split())
        if word_count > 10:
            continue
        # if comment_body == "[removed]" or comment_body == "[deleted]":
        #     continue
        if "[removed]" in comment_body or "[deleted]" in comment_body:
            continue

        # ups = comment["data"].get("ups",1)
        # print(f"{index} - Ups: {ups}")
        # print(f"{index}")
        
        comments.append({
            "index": str(index),
            "author": comment["data"]["author"],
            # "comment": comment["data"]["body"],
            "comment": comment_body,
            # "author": comment["data"].get("author", ""),
            # "comment": comment["data"].get("body", ""),
            "ups": str(comment["data"]["ups"]),
            "utc_timestamp": comment["data"]["created_utc"],
            "relative_time": utc_to_relative_time(comment["data"]["created_utc"]),
            "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment["data"]["created_utc"]))            
        })
        
        # Check if three comments have been appended
        if len(comments) == max_num_of_comments:
            break
    print(f"Finished getting comments from {url}...")
    return comments

def combine_post_comments(post, comments, post_index):
    # what is the type of post and comments?
    # print(type(post)) # dict
    # print(type(comments)) # list of dict
    merged_post = post
    merged_post["comments"] = comments
    file_name = f"resources\\temp\\post_{post_index}.json"
    save_json(merged_post, file_name)
    clean_json_file(file_name, file_name)
    json_data = load_json_file(file_name)
    return json_data

def get_reddit_data(url="https://www.reddit.com/r/AskReddit/top.json?t=day", num_posts=1, num_comments=30):
  
    # Variables to choose from...
    # url = "https://www.reddit.com/r/AmItheAsshole/top.json?t=day"
    # url = "https://www.reddit.com/r/AskReddit/top.json?t=day"
    # url = "https://www.reddit.com/r/mildlyinfuriating/top.json?t=day"
    # url = "https://www.reddit.com/subreddits/popular.json"
    # post_num = 0  # first (top most post) (usually <25 posts)
    
    # Get Reddit posts from url
    reddit_posts = get_posts(url)
    # get all posts and their comments
    json_posts = []
    for i, post in enumerate(reddit_posts):
        if i >= num_posts:
            break
        post_comment = get_comments(post['url'], num_comments)
        combined_post = combine_post_comments(post, post_comment, i)
        json_posts.append(combined_post)
    return json_posts
  
if __name__ == "__main__":
    get_reddit_data()