from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# -------------------------------
# Selenium Setup (Headless Mode)
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 20)

# -------------------------------
# URLs to Scrape
# -------------------------------
urls = [

"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.donite%20plastics%20ltd.org-ed305c26-a9a6-488e-9f12-960365ab530b.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.device%20technologies%20inc.org-d65144c1-d70f-44d7-9833-bcd3a3d802d6.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.duflot%20industrie%20sas.org-f1d7b0a5-c859-4eb7-a457-84d12e3f08bb.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.dupont%20tedlar%20kevlar%20and%20nomex.org-8ec8f2bd-d9ce-4f30-aa31-c95a1b609e11.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.duracote%20corporation.org-56e32c0c-de27-40da-955d-6a4aeb859c9c.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.dylan%20aerospace.org-1ccc0e81-437b-4845-afde-39fe22b9123d.html",
"https://www.aircraftinteriorsexpo.com/en-gb/exhibitor-directory/exhibitor-details.eam%20worldwide.org-c021c6fb-1f45-4db6-8974-59a444ed6af3.html",


]

# -------------------------------
# Prepare CSV
# -------------------------------
with open("aix_companies_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Email", "Source URL"])

    for index, url in enumerate(urls, start=1):
        print(f"\nProcessing {index}/{len(urls)}: {url}")
        driver.get(url)

        company_name = "Not Found"
        email = "Not Found"

        # Wait for the company name h1 to appear (JS-rendered page)
        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.details-header h1.wrap-word")
            ))
        except TimeoutException:
            print("  ⚠ Timed out waiting for page content")

        time.sleep(2)  # small buffer for full render

        # ── Company Name ────────────────────────────────────────────────────
        # <div class="details-header"> → <h1 class="wrap-word">TEAM PLASTIQUE</h1>
        try:
            name_el = driver.find_element(By.CSS_SELECTOR, "div.details-header h1.wrap-word")
            company_name = name_el.text.strip()
        except NoSuchElementException:
            pass

        # ── Email ───────────────────────────────────────────────────────────
        # <div class="exhibitor-details-contact-us-links">
        #   <a href="mailto:contact@teamplastique.com" ...>
        try:
            email_el = driver.find_element(
                By.CSS_SELECTOR,
                "div.exhibitor-details-contact-us-links a[href^='mailto:']"
            )
            href = email_el.get_attribute("href")   # "mailto:contact@teamplastique.com"
            email = href.replace("mailto:", "").strip()
        except NoSuchElementException:
            pass

        writer.writerow([company_name, email, url])
        print(f"  ✔ Company : {company_name}")
        print(f"  ✔ Email   : {email}")

driver.quit()
print("\n✅ Done! Data saved to aix_companies_data.csv")