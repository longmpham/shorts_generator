import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables from .env file
# load_dotenv()




async def main():
    load_dotenv()
    async with async_playwright() as p:
        # browser = await p.chromium.launch()
        # Use playwright.chromium, playwright.firefox or playwright.webkit
        browser = await p.firefox.launch(headless=False)
        page_size = {
            "width": 1920,
            "height": 1080,
        }
        page = await browser.new_page(viewport=page_size)
        await page.goto("https://www.tiktok.com/explore")
        print(await page.title())
        # page.screenshot(path="example.png")
        
        # Log in
        # Click the "Log in" button using a locator
        button_login = 'button:has-text("Log in")'
        await page.locator(button_login).nth(0).click(button="left") # finds 2 log in instances
        # await page.locator(button_login).click(button="left")
        
        # click by email username etc.
        login_with_email_button_xpath = "/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div/div/a[2]"
        await page.locator("xpath=" + login_with_email_button_xpath).click()
        
        # Click Log in with email or username
        login_with_email_text_xpath = "/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[1]/a"
        await page.locator("xpath=" + login_with_email_text_xpath).click()
        
        # Access the environment variables using os.environ
        username = os.environ.get("USER")
        password = os.environ.get("PASSWORD")
        # Find the input element with name="username" and enter the email
        username_locator = page.locator('input[type="text"]')
        await username_locator.fill(username)
        await page.wait_for_timeout(1000)
        
        # Find the input element with name="username" and enter the email
        password_locator = page.locator('input[type="password"]')
        await password_locator.fill(password)
        await password_locator.press("Enter")
        
        button_pets_and_nature = 'span:has-text("Pets and Nature")' 
        await page.locator(button_pets_and_nature).click(button="left")
            # button="left", modifiers=["Shift"], position={"x": 23, "y": 32}
            
        input()
            
            
        await browser.close()

    
asyncio.run(main())