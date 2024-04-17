import asyncio
from playwright.async_api import async_playwright, Browser
import sys
import json
import os
import time
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime as dt
from typing import List

# Load environment variables from .env file
load_dotenv()
reddit_user = os.getenv("REDDIT_USER")
reddit_pw = os.getenv("REDDIT_PW")

MAX_COMMENT_LIMIT = 10

async def utc_to_relative_time(utc_timestamp):
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

async def save_to_json(filename, data):        
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return

def load_json_file(file_path):
    data = {}
    with open(file_path) as file:
        data = json.load(file)
    # print(data)
    return data

async def scroll_down(page):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    await asyncio.sleep(1)  # Adjust the sleep 1ime (in seconds) to control the scrolling speed

async def get_reddit_title(url: str) -> None:
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await login(page)
        
        await page.goto(url)
        # title of the page
        # title = page.locator("shreddit-post") # old and broken now DNE
        # try:
        #     title = page.get_by_test_id("post-container")
        #     # await title.screenshot(path="./resources/reddit/post.png")
        #     # await page.close()
        # except Exception as e:
        #     print("There was an issue grabbing 'title = page.get_by_test_id('post-container')'")
        #     print("Trying shreddit-post way")

        try:
            title = page.locator("shreddit-post")
            await title.screenshot(path="./resources/reddit/post.png")
            await page.close()
        except Exception as e:
            print("There was an issue grabbing 'title = page.locator('shreddit-post')'")
            await page.close()
            exit()        
        
        # await title.screenshot(path="./resources/reddit/post.png")
        # await page.close()

async def get_reddit_title_screenshot(page: Browser, posts, num_posts: int) -> None:
    
    for index, post in enumerate(posts[:num_posts]):
        url = post['url']
        print(f"getting a top post: {url}")
        await asyncio.sleep(5)

        await page.goto(url)
        await asyncio.sleep(1)
        try:
            title = page.locator("shreddit-post")
            await title.screenshot(path=f"./resources/reddit/post-{index}.png")
            # await page.close()
        except Exception as e:
            print(f"There was an issue grabbing 'title = page.locator('shreddit-post')': {e}")
            # await page.close()
            # exit()        


async def get_comments(page, url, max_num_of_comments=30):
    
    print(f"Geting comments from {url}...")
    url = url + ".json"
    # await page.set_viewport_size({"width": int(485), "height": 800})
    await page.goto(url)    
    data = await page.evaluate("() => { return JSON.parse(document.body.innerText); }")

    # Save json post data
    # await save_to_json("./resources/reddit/full_post.json", data)

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
            "relative_time": await utc_to_relative_time(comment["data"]["created_utc"]),
            "date_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment["data"]["created_utc"]))            
        })
        
        # Check if three comments have been appended
        if len(comments) == max_num_of_comments:
            break
    print(f"Finished getting comments from {url}...")
    return comments

async def combine_post_comments(post, comments, post_index):
    # what is the type of post and comments?
    # print(type(post)) # dict
    # print(type(comments)) # list of dict
    merged_post = post
    merged_post["comments"] = comments
    file_name = f"./resources/reddit/post_{post_index}.json"
    # Save json post data
    await save_to_json(file_name, merged_post)
    # save_json(merged_post, file_name)
    # clean_json_file(file_name, file_name)
    json_data = load_json_file(file_name)
    return json_data

async def parse_json_data(page, reddit_posts, num_posts=1, num_comments=30):
    # get all posts and their comments
    json_posts = []
    for i, post in enumerate(reddit_posts):
        if i >= num_posts:
            break
        post_comment = await get_comments(page, post['url'], num_comments)
        combined_post = await combine_post_comments(post, post_comment, i)
        json_posts.append(combined_post)
    return json_posts

async def get_json_data(page: Browser,  url: str, num_posts=10) -> None:
    # page = await context.new_page()
    # await page.set_viewport_size({"width": int(485), "height": 800})
    base_url="https://www.reddit.com/r/AskReddit/top.json?t=day"
    await page.goto(base_url)
    
    data = await page.evaluate("() => { return JSON.parse(document.body.innerText); }")

    # Save json post data
    await save_to_json("./resources/reddit/full_post.json", data)
        
    posts = []
    for _ in range(num_posts):
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
                "relative_time": await utc_to_relative_time(utc_timestamp),
                "url": url,
                "date_time": utc_time,
            })
            print(f"Getting posts from {url}...")
    print(f"finished getting posts from {base_url}")

    await asyncio.sleep(1)

    # await page.close()
    return posts

async def login(page: Browser,  url="https://www.reddit.com/login") -> None:
    # page = await context.new_page()
    await page.set_viewport_size({"width": int(485), "height": 800})
    await page.goto(url)
    await asyncio.sleep(1)
    await page.locator("input[name=\"username\"]").fill(reddit_user)
    await asyncio.sleep(1)
    await page.locator("input[name=\"password\"]").fill(reddit_pw)
    await asyncio.sleep(1)
    await page.get_by_role("button", name="Log In").click()
    # await page.keyboard.press('Enter')
    for i in range(15,0,-1):
        print(f"{i}...")
        await asyncio.sleep(1)
    # let the login take place.
    # for some reason it wont idle.
    # await page.wait_for_url("https://www.reddit.com/")
    # await page.wait_for_load_state("networkidle")
    
    # for some reason the context doesn't hold so dont close the page.
    # await page.close()

async def capture(context: Browser,  url: str) -> None:
    page = await context.new_page()
    await page.set_viewport_size({"width": int(485), "height": 800})


    await page.goto(url)
    
    for _ in range(1):
        await scroll_down(page)
        await scroll_down(page)
        try:
            span = await page.wait_for_selector('span:has-text("View more comments")')
            # Click the span element
            await span.click()        
        except: 
            print("couldn't find button")
    
    # for some reason i have to keep this for the minus buttons to prompt
    await asyncio.sleep(1)
    
    # Find all buttons matching the specified attributes
    buttons = await page.query_selector_all('button[aria-controls="comment-children"][aria-expanded="true"][aria-label="Toggle Comment Thread"]')

    # Click each button
    for button in buttons:
        # print(f"clicking {button}...")
        await button.click()

    title = page.locator("shreddit-post")
    
    # title of the page
    await title.screenshot(path="resources\\temp\\post.png")

    # comments = page.locator("shreddit-comment")
    comments = await page.locator('//*[@id="comment-tree"]/shreddit-comment').all() # works
    # comments = await page.locator('//*[@id="comment-tree"]/shreddit-comment[not(.//shreddit-comment)]').all()

    # comments = await page.locator("shreddit-comment:not(:has(> shreddit-comment[parentid]))").all()
    # score_value = await page.evaluate('(selector) => document.querySelector(selector).getAttribute("score")', "#comment-tree > shreddit-comment:nth-child(13)") # returns a number

    # Create a list to store tuples of (score, comment_element)
    comment_list = []
    
    # Extract score and element for each comment
    for comment in comments:
        # score = int(await comment.get_attribute("score"))
        score = await comment.evaluate('(element) => element.getAttribute("score")')
        print(score)
        
        comment_list.append((int(score), comment))
    # Sort comments based on score
    sorted_comments = sorted(comment_list, key=lambda x: x[0], reverse=True)
    # print(sorted_comments)

    # Take screenshots of the first three comments
    for i in range(min(3, len(sorted_comments))):
        await sorted_comments[i][1].screenshot(path=f"resources\\temp\\comment-{i+1}.png")
        
    # print(f"Found {count} comments")
    

    # for i in range(count):
    #     print(f"printing comment: {i+1}")
    #     await comments.nth(i).screenshot(path=f"resources\\temp\\comment-{i}.png")

    #     if i+1 == MAX_COMMENT_LIMIT:
    #         # print(f"Screened {MAX_COMMENT_LIMIT} images, stopping.")
    #         break


async def get_reddit_data(reddit_url: str, num_posts=10, num_comments=30) -> List:
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # browser = await p.chromium.launch()
        
        # log in
        print("logging in...")
        await login(page, "https://www.reddit.com/login")
        
        print("getting json data...")
        posts = await get_json_data(page, reddit_url, num_posts)
        
        # Get screenshots
        print("Getting screenshots...")
        await get_reddit_title_screenshot(page, posts, num_posts)
        
        # now that we have the master json, we parse the goodies
        print("parsing json data for each post...")
        json_posts = await parse_json_data(page, posts, num_posts, num_comments)
        
        # capture title and comments screenshots
        # await capture(page, reddit_url)    
        
        await page.close()
        return json_posts

if __name__ == "__main__":
    # Check if a URL argument is provided
    if len(sys.argv) == 2:
        print("Usage: python <filename> <url>")
        reddit_url = sys.argv[1]
        # sys.exit(1)
    else:
        reddit_url = "https://www.reddit.com/r/AskReddit/top.json?t=day"

    # Call main function with the provided URL
    asyncio.run(get_reddit_data(reddit_url, num_posts=3))
