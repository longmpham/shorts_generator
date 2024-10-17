import asyncio
from playwright.async_api import async_playwright

async def scrape_tiktok_funny_videos():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run without a UI
        page = await browser.new_page()

        # Navigate to TikTok's trending page
        await page.goto('https://www.tiktok.com/trending')

        # Wait for the "Continue as a guest" button and click it
        await page.wait_for_selector('button[data-e2e="guest-continue-button"]', timeout=60000)
        await page.click('button[data-e2e="guest-continue-button"]')

        # Wait for a moment to ensure the page loads completely
        await page.wait_for_timeout(2000)

        # Scroll to the bottom of the page to load more videos
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for at least 10 video elements to be present
        await page.wait_for_function("document.querySelectorAll('div.tiktok-1s72j7h-DivVideoContainer').length >= 10", timeout=60000)

        # Extract video details
        videos = await page.evaluate('''() => {
            const videoElements = Array.from(document.querySelectorAll('div.tiktok-1s72j7h-DivVideoContainer'));
            return videoElements.map(video => {
                const title = video.querySelector('h3.tiktok-1s72j7h-H3VideoTitle')?.innerText || 'No Title';
                const url = video.querySelector('a.tiktok-1s72j7h-Anchor')?.href || 'No URL';
                const likes = video.querySelector('strong.tiktok-1s72j7h-Strong')?.innerText || 'No Likes';
                return { title, url, likes };
            });
        }''')

        # Get the top 10 funniest videos (this may require additional filtering based on your criteria)
        top10_funny_videos = videos[:10]

        # Display the results
        print('Top 10 Funniest TikTok Videos of the Day:')
        for index, video in enumerate(top10_funny_videos):
            print(f"{index + 1}. Title: {video['title']}, URL: {video['url']}, Likes: {video['likes']}")

        # Close the browser
        await browser.close()

# Run the async function
if __name__ == "__main__":
    asyncio.run(scrape_tiktok_funny_videos())
