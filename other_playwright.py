import asyncio
from playwright.async_api import async_playwright, Browser

MAX_COMMENT_LIMIT = 10

async def scroll_down(page):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

async def capture(browser: Browser,  url: str) -> None:
    page = await browser.new_page()

    await page.goto(url)
    
    for _ in range(3):
        await scroll_down(page)
        await asyncio.sleep(2)  # Adjust the sleep time (in seconds) to control the scrolling speed
        try:
            # view_more_comments_button = 'span:has-text("View more comments")'
            view_more_comments_button_xpath = "/html/body/shreddit-app/div/div[2]/faceplate-batch/faceplate-tracker/shreddit-comment-tree/faceplate-partial/div[1]/button"
            # await page.locator(view_more_comments_button).click()
            await page.locator("xpath=" + view_more_comments_button_xpath).click()
        except: 
            print("couldn't find button")

    
    posts = page.locator("shreddit-post")
    # posts = page.get_by_test_id("post-container") # sometimes works.

    await posts.screenshot(path="resources\\temp\\post.png")

    # this does not respect comment-nesting
    # comments = page.locator(".Comment") # doesnt work
    comments = page.locator("shreddit-comment")
    count = await comments.count()
    print(f"Found {count} comments")
    
    # await asyncio.sleep(120)
    
    await comments.nth(22).screenshot(path=f"resources\\temp\\comment-{22}.png")
    await comments.nth(23).screenshot(path=f"resources\\temp\\comment-{23}.png")
    await comments.nth(24).screenshot(path=f"resources\\temp\\comment-{24}.png")
    
    
    # for i in range(count):
    #     print(f"printing comment: {i+1}")
    #     await comments.nth(i).screenshot(path=f"resources\\temp\\comment-{i}.png")

    #     if i+1 == MAX_COMMENT_LIMIT:
    #         # print(f"Screened {MAX_COMMENT_LIMIT} images, stopping.")
    #         break


async def main() -> None:
    reddit_url = "https://www.reddit.com/r/AskReddit/comments/155twk3/whats_the_fastest_way_youve_ever_seen_a_new/"
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False)
        browser = await p.chromium.launch()
        await capture(browser, reddit_url)
        await browser.close()

asyncio.run(main())