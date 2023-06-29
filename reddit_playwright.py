import asyncio
from playwright.async_api import async_playwright, Browser

MAX_COMMENT_LIMIT = 10

async def capture(browser: Browser,  url: str) -> None:
    page = await browser.new_page()

    await page.goto(url)
    posts = page.locator("shreddit-post")
    # posts = page.get_by_test_id("post-container") # sometimes works.

    await posts.screenshot(path="resources\\temp\\post.png")

    # this does not respect comment-nesting
    # comments = page.locator(".Comment") # doesnt work
    comments = page.locator("shreddit-comment")
    count = await comments.count()
    print(f"Found {count} comments")
      
    for i in range(count):
        print(f"printing comment: {i+1}")
        await comments.nth(i).screenshot(path=f"resources\\temp\\comment-{i}.png")

        if i+1 == MAX_COMMENT_LIMIT:
            # print(f"Screened {MAX_COMMENT_LIMIT} images, stopping.")
            break


async def main() -> None:
    reddit_url = "https://www.reddit.com/r/mildlyinfuriating/comments/14l81aw/after_you_cross_the_road_in_some_american_cities/"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        await capture(browser, reddit_url)
        await browser.close()

asyncio.run(main())