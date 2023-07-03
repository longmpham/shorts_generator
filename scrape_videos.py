import requests
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_pexels_videos(search_term, max_num_videos=10):
    # Set up Selenium WebDriver
    # Create a Chrome WebDriver service
    chromedriver_path = 'C:\\Program Files\\Google\\Chrome\\chromedriver.exe'
    service = Service(chromedriver_path)
    adblocker_path = "C:\\Users\\longp\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cjpalhdlnbpafiamejdnhcphjbkeiagm\\1.49.2_0.crx"
    chrome_options = Options()
    chrome_options.add_extension(adblocker_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Replace with path to your WebDriver
    
    
    # Load the webpage
    url = f'https://www.pexels.com/search/videos/{search_term}/'
    driver.get(url)
    
    # Define the number of times to scroll
    scroll_times = 5

    # Scroll to the bottom of the page multiple times
    for _ in range(scroll_times):
        # Execute JavaScript to scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for 3 seconds before scrolling again
        time.sleep(3)

    # Extract the page source after dynamic content has loaded
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all video tags with src attribute
    video_tags = soup.find_all('source', {'src': True})
    # video_tags = soup.find_all('video')
    # print(video_tags)
    # Create directory to save videos
    save_directory = f"resources\\background_videos\\scraper\\{''.join(search_term.split())}"
    os.makedirs(save_directory, exist_ok=True)

    # Download the videos
    for i, video_tag in enumerate(video_tags):
        
        video_url = video_tag['src']
        print(video_url)
        video_name = f"{search_term} {i}.mp4"
        # video_name = f"{''.join(search_term.split())}_{i}.mp4" # no spaces 
        save_path = os.path.join(save_directory, video_name)

        response = requests.get(video_url)
        with open(save_path, 'wb') as f:
            f.write(response.content)
          
        if i >= max_num_videos: 
          break



    print('All videos downloaded successfully.')

# Example usage
search_term = input("Enter the search term: ")
max_num = input("Enter the number of videos: ")
scrape_pexels_videos(search_term, int(max_num))
