#https://www.seatrade-europe.com/expo-conference/exhibitor-list  scrapper

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException


# Set up Selenium with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background (remove if you want to see the browser)  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--disable-extensions")  # Disable extensions

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the webpage
urls = ['https://www.smm-hamburg.com/platform/SM24/corporation/a-spe-europe-i-mianowski-spolka-jawna@4183?cHash=59856cc639ba23539f81ed484533c51f'       
]
for url in urls:
    driver.get(url)
    print(f"Link opened successfully: {url}")  # Print confirmation on terminal

# Wait for the page to fully load
    time.sleep(1)  # Adjust time if needed
    
    try:
        # Find all 'a' tags inside the list
        anchor_tags = driver.find_elements(By.CSS_SELECTOR, "ul.list-unstyled.list-inline a")

        # Loop through each anchor tag and print href attribute
        for anchor in anchor_tags:
            link = anchor.get_attribute("href")
            print(link if link else "N/A")
    except:
        print("N/A")  # In case of any errors


# Close the browser
driver.quit()







