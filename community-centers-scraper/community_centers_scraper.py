import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

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
urls = ['https://www.lubavitch.com/centers/north-america/usa/az/phoenix/',
    
        ]

# Prepare CSV file for writing
with open('chabad_centers.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Address', 'Phone Number', 'Website'])  # Write header

    for url in urls:
        driver.get(url)
        print(f"Link opened successfully: {url}")  # Print confirmation on terminal

        # Wait for the page to fully load
        time.sleep(1)  # Adjust time if needed

        # Extract multiple names
        names = []
        try:
            name_elements = driver.find_elements(By.CLASS_NAME, "chabad-house")  # Locate by class name
            for name_element in name_elements:
                names.append(name_element.text.strip() if name_element.text.strip() else "NA")
        except:
            names.append("NA")

        # Extract multiple addresses
        addresses = []
        try:
            address_elements = driver.find_elements(By.CLASS_NAME, "fade-txt")  # Locate by class name
            for address_element in address_elements:
                addresses.append(address_element.text.strip().replace("\n", " ") if address_element.text.strip() else "NA")
        except:
            addresses.append("NA")

        # Extract multiple phone numbers
        phone_numbers = []
        try:
            phone_elements = driver.find_elements(By.XPATH, "//div[@class='phone']/span[@class='fade-txt']")  # Locate by XPath
            for phone_element in phone_elements:
                phone_numbers.append(phone_element.text.strip() if phone_element.text else "NA")
        except:
            phone_numbers.append("NA")

        # Extract multiple website links
        links = []
        try:
            link_elements = driver.find_elements(By.XPATH, "//span[@class='fade-txt-txt']/a")  # Locate by XPath
            for link_element in link_elements:
                links.append(link_element.get_attribute("href") if link_element.get_attribute("href") else "NA")
        except:
            links.append("NA")

        # Write the extracted data to the CSV file
        for name, address, phone, link in zip(names, addresses, phone_numbers, links):
            writer.writerow([name, address, phone, link])

# Close the browser
driver.quit()
