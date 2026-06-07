import csv
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# catch both Selenium and urllib3 timeouts
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import ReadTimeoutError

# --- SOLUTION 3: bump the underlying HTTP‐client timeout to 5 minutes ---

# --- CONFIGURATION ---
PRODUCT_URLS = [
"https://www.aircraftspruce.com/catalog/pnpages/15-06807.php",
"https://www.aircraftspruce.com/catalog/pnpages/15-06295.php",
"https://www.aircraftspruce.com/catalog/pnpages/15-05845.php",
"https://www.aircraftspruce.com/catalog/rtxpages/rotax-15-00133.php",
"https://www.aircraftspruce.com/catalog/rtxpages/rotax-15-00668.php",
"https://www.aircraftspruce.com/catalog/pnpages/15-09106.php",
"https://www.aircraftspruce.com/catalog/pnpages/15-02845.php",

   

]
LOGIN_URL   = "https://www.aircraftspruce.com/account.html"
OUTPUT_CSV  = "AirCraft.csv"

# --- 1) START CHROME (non-headless, images ON for login) ---
chrome_opts = Options()
chrome_opts.add_argument("--no-sandbox")
chrome_opts.add_argument("--disable-dev-shm-usage")
chrome_opts.add_argument("--disable-gpu")
chrome_opts.add_argument("--disable-extensions")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_opts
)

wait = WebDriverWait(driver, 20)

# 2) NAVIGATE TO LOGIN PAGE
driver.get(LOGIN_URL)
print("\n⚠️  Chrome opened. Log in and solve the CAPTCHA if prompted.")
print("→ Once you see your account page (e.g. ‘Sign Out’ link), press ENTER here...")
input()

# 3) BLOCK IMAGES FROM HERE ON OUT (speed up scraping)
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setBlockedURLs", {
    "urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg"]
})
print("🖼️  Images now blocked via CDP. Beginning scrape…\n")

# 4) OPEN CSV FOR OUTPUT
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Product_Name",
        "Overview",
        "Part#",
        "MFR Model#",
        "Image_Link",
        "Regular_Price",
        "Net_Price",
        "Stock_Status",
        "Source_URL"
    ])

    def try_get(fn, default="NA"):
        try:
            return fn().strip()
        except:
            return default

    # 5) SCRAPE EACH PRODUCT PAGE
    for idx, url in enumerate(PRODUCT_URLS, start=1):
        try:
            driver.get(url)
            print(f"{idx}. Loading {url}")
            time.sleep(2)  # let JS render price

            title        = try_get(lambda: driver.find_element(By.TAG_NAME, "h2").text)
            overview     = try_get(lambda: driver.find_element(By.XPATH, "//td[@valign='top']").text)
            stock_status = try_get(lambda: driver.find_element(By.CLASS_NAME, "prStockStatus").text)
            image_link   = try_get(lambda: driver.find_element(
                                By.CSS_SELECTOR, "a[data-fancybox='productMainImage']"
                             ).get_attribute("href"))

            # split the <div id="np"> into two lines
            raw_np = try_get(lambda: driver.find_element(By.ID, "np").text)
            lines = raw_np.splitlines()
            if len(lines) >= 2:
                regular_price = lines[0].split()[0]
                net_price     = lines[1].replace("Net", "").strip()
            else:
                regular_price = net_price = raw_np

            # Part# and MFR Model#
            try:
                parts = driver.find_element(By.CLASS_NAME, "prModel").text.split("\n")
                part_num = parts[0] if parts else "NA"
                mfr_mod  = parts[1] if len(parts) > 1 else "NA"
            except:
                part_num = mfr_mod = "NA"

            writer.writerow([
                title,
                overview,
                part_num,
                mfr_mod,
                image_link,
                regular_price,
                net_price,
                stock_status,
                url
            ])
        except (TimeoutException, ReadTimeoutError) as e:
            print(f"⏱️ Timeout loading {url}, writing placeholder and continuing.")
            writer.writerow([
                "TIMEOUT_ERROR",  # Product_Name
                "TIMEOUT_ERROR",  # Overview
                "TIMEOUT_ERROR",  # Part#
                "TIMEOUT_ERROR",  # MFR Model#
                "TIMEOUT_ERROR",  # Image_Link
                "TIMEOUT_ERROR",  # Regular_Price
                "TIMEOUT_ERROR",  # Net_Price
                "TIMEOUT_ERROR",  # Stock_Status
                url               # Source_URL
            ])
        finally:
            f.flush()

print(f"\n🎉 Done! Your data (including any timeouts) is in {OUTPUT_CSV}")
driver.quit()
