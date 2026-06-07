from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# -------------------------------
# Selenium Setup (Headless Mode)
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # Remove this if you want to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# -------------------------------
# URLs to Scrape
# -------------------------------
urls = [
"https://yourmaritime.com/directory/ventocean",
"https://yourmaritime.com/directory/bluemarine",
"https://yourmaritime.com/directory/rnt-marine-electronics",
"https://yourmaritime.com/directory/aria-ship-supply",
"https://yourmaritime.com/directory/blue-matter-marine-consulting",

        
]

# -------------------------------
# Prepare CSV File for Writing
# -------------------------------
with open('companies_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name', 'Email', 'Source URL'])  # Write header

    # -------------------------------
    # Process Each URL
    # -------------------------------
    for index, url in enumerate(urls, start=1):
        print(f"Processing {index}/{len(urls)}: {url}")
        driver.get(url)

        time.sleep(2)  # Wait for the page to load completely

        # Default values
        company_name = "Not Found"
        email = "Not Found"

        # Extract Company Name
        try:
            company_element = driver.find_element(By.CSS_SELECTOR, "h1.display-3.text-black.mb-3 span[itemprop='name']")
            company_name = company_element.text.strip()
        except NoSuchElementException:
            pass

        # Extract Email
        try:
            email_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='email'] a")
            email = email_element.text.strip()
        except NoSuchElementException:
            pass

        # Write Data Immediately to CSV
        writer.writerow([company_name, email, url])
        print(f"✔ Done: {company_name}, {email}\n")

# Close Browser
driver.quit()

print("✅ Data extraction completed! Saved to companies_data.csv")
