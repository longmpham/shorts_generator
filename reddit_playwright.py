import asyncio
from playwright.async_api import async_playwright, Browser
import sys

MAX_COMMENT_LIMIT = 10

async def scroll_down(page):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    await asyncio.sleep(1)  # Adjust the sleep time (in seconds) to control the scrolling speed


async def get_reddit_title(browser: Browser,  url: str) -> None:
    page = await browser.new_page()
    await page.goto(url)
    # title of the page
    title = page.locator("shreddit-post")
    await title.screenshot(path="resources\\temp\\post.png")

async def capture(browser: Browser,  url: str) -> None:
    page = await browser.new_page()
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
    await asyncio.sleep(3)
    
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


async def main(reddit_url: str) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # browser = await p.chromium.launch()
        await capture(browser, reddit_url)
        # await get_reddit_title(browser, reddit_url)
        await browser.close()

if __name__ == "__main__":
    # Check if a URL argument is provided
    if len(sys.argv) == 2:
        print("Usage: python <filename> <url>")
        reddit_url = sys.argv[1]
        # sys.exit(1)
    else:
        reddit_url = "https://www.reddit.com/r/AskReddit/comments/1bmnayh/what_is_the_biggest_lie_successfully_sold_by_the/"

    # Call main function with the provided URL
    asyncio.run(main(reddit_url))
