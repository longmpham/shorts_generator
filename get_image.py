import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def get_image_from_answer(keyword, picture_desc):
    # Set the path to the chromedriver executable
    chromedriver_path = "C:\\Program Files\\Google\\Chrome\\chromedriver.exe"
    filename = f"{keyword}.png"
    # Path to the adblocker extension file (.crx or .zip)
    adblocker_path = "C:\\Users\\longp\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cjpalhdlnbpafiamejdnhcphjbkeiagm\\1.49.2_0.crx"
    download_directory = os.path.join(os.getcwd(), "resources", "screenshots", f"{keyword}")
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Create a Chrome WebDriver service
    service = Service(chromedriver_path)

    # Set the download filename with counter and original file extension
    counter = 1
    # download_filename = f"{filename}_{counter}.png"  # e.g., dog_1.png

    # Check if the filename already exists and increment the counter
    # while os.path.exists(os.path.join(download_directory, download_filename)):
    #     counter += 1
    #     download_filename = f"{filename}_{counter}.png"


    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_extension(adblocker_path)
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    # "download.default_filename": filename,  # Specify the custom file name
})

    # Start the WebDriver
    driver = webdriver.Chrome(service=service,  options=chrome_options)
    # driver = webdriver.Chrome() # should just work too
    
    # Open the Pexels website
    driver.get("https://www.craiyon.com/") # Free online AI image generator from text

    time.sleep(1)
    
    # Click "Photo" Button for type of drawing
    wait = WebDriverWait(driver, 30)  # Maximum wait time of 10 seconds
    image_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/button[3]")))
    image_element.click()
    
    time.sleep(1)

    # Search for the keyword
    # Wait for the image element to appear
    wait = WebDriverWait(driver, 30)
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "prompt")))
    # search_box = driver.find_element(By.ID, "search")
    search_box.send_keys(keyword + picture_desc)
    search_box.send_keys(Keys.ENTER)
    print("sent keys")

    time.sleep(1)

    # Scroll down the webpage
    driver.execute_script("window.scrollTo(0, 450);")
    print("sent scroll")
    
    time.sleep(1)
    
    # First image of 9 generated images
    wait = WebDriverWait(driver, 300)
    image_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//html/body/div/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div[1]/img")))
    image_element.click()
    print("waiting for images to render")
    
    time.sleep(1)

    # Upscale button
    wait = WebDriverWait(driver, 30)
    upscale_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/button[1]")))
    upscale_button.click()
    print("clicked upscale")
    
    # Wait for the upscaled image
    wait = WebDriverWait(driver, 300)
    large_image_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div/img")))
    # screenshot = large_image_element.screenshot_as_png
    
    # Screenshot button
    # screenshot_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/button[2]")
    # wait = WebDriverWait(driver, 30)
    
    # Download button
    # download_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[2]/div/div[2]/div[1]/div/button[2]")))
    # screenshot_button.click()
    wait = WebDriverWait(driver, 300)
    # download_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div/div[2]/button[2]")))
    download_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/main/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div/div[2]/button[2]")))
    download_button.click()
    
    time.sleep(1)
    
    # Save the screenshot to a file
    screenshot_folder = os.path.join(os.getcwd(), 'resources', 'screenshots')
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    screenshot_path = os.path.join(screenshot_folder, f'{keyword}.png')
    # with open(screenshot_path, 'wb') as f:
    #     f.write(screenshot)
    
    # Exit Selenium
    driver.quit()

    # Return the path of the saved image
    return screenshot_path


keyword = "dogs"
picture_desc = ", not a person but a place or thing"
get_image_from_answer(keyword, picture_desc)