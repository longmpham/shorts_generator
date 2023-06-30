import asyncio
from playwright.async_api import async_playwright, Browser

MAX_COMMENT_LIMIT = 10

async def capture(browser: Browser,  url: str) -> None:
    page = await browser.new_page()

    await page.goto(url)
    # gifs = page.locator("img")
    # page.wait
    # await page.wait_for_load_state()
    await page.wait_for_timeout(5*1000)
    
    number_scrolls = 5
    for i in range(number_scrolls):
        # Scroll to the bottom of the page
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2*1000)
    
    gifs = await page.query_selector_all("img")

    for gif in gifs:
        src = str(await gif.get_attribute("src"))
        print(src)
    # count = await gifs.count()
    # print(f"Found {count} gifs")
    # print(gifs)

    # for i in range(count):
    #     src = str(await gifs.nth(i).get_attribute("src"))
    #     print(f"Loaded image: {src}")
        

    
    
    return

async def main() -> None:
    search_term = "dogs"
    url = f"https://giphy.com/explore/{search_term}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        await capture(browser, url)
        await browser.close()

asyncio.run(main())