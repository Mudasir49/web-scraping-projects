import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
NUM_SUBMISSIONS = 100  # Change this value to control how many times the form is submitted
# ---------------------

def submit_one_form(driver, wait):
    """
    Executes one complete form submission pass.
    """
    url = "https://forms.office.com/pages/responsepage.aspx?id=n7oos1aYJ02xeF0Vfd8dkz2uvVnqaY9Lu6hyF3oYU4hUQ0NPOFZEUEtaV1pFSVBDQVdMWFExQzZBSCQlQCN0PWcu&route=shorturl"
    print(f"Navigating to {url}")
    driver.get(url)
    
    # --- Screen 1: Start ---
    print("Waiting for Start button...")
    time.sleep(3) # Give it a moment to render
    
    buttons = driver.find_elements(By.TAG_NAME, "button")
    
    # Strategy: Iterate through buttons and find one with "Start" text
    clicked = False
    for b in buttons:
        txt = b.text.strip().lower()
        if "start" in txt or "starten" in txt:
            print(f"Found target button: '{b.text}'")
            try:
                # Scroll into view first
                driver.execute_script("arguments[0].scrollIntoView(true);", b)
                time.sleep(0.5)
                b.click()
                print("Clicked Start (Standard)")
                clicked = True
                break
            except Exception as e:
                print(f"Standard click failed ({e}). Trying JS click...")
                try:
                    driver.execute_script("arguments[0].click();", b)
                    print("Clicked Start (JS)")
                    clicked = True
                    break
                except Exception as js_e:
                    print(f"JS click failed: {js_e}")
    
    if not clicked:
        print("Text search failed. Trying to click the button with class 'css-148' that has text...")
        # Fallback: specific class css-148 and non-empty text
        for b in buttons:
            if "css-148" in b.get_attribute("class") and b.text.strip():
                 print(f"Fallback clicking button with class {b.get_attribute('class')} and text '{b.text}'")
                 driver.execute_script("arguments[0].click();", b)
                 clicked = True
                 break

    if not clicked:
         raise Exception("Could not successfully click the Start button.")
    
    time.sleep(2) # transition
    
    # --- Screen 2: Intro / Next ---
    print("Waiting for first Next button...")
    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next'], button[aria-label='Weiter']")))
    next_btn.click()
    print("Clicked Next (1)")
    
    # --- Screen 3: Age & Biofach ---
    print("Waiting for Age question...")
    
    # Wait for the choices to load
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='radio'], [role='radio']")))
    except:
        print("Timed out waiting for radios.")
    
    possible_radios = driver.find_elements(By.CSS_SELECTOR, "[data-automation-id='radio']")
    
    if not possible_radios:
        # Fallback to role since sometimes it's div[role='radio']
        possible_radios = driver.find_elements(By.CSS_SELECTOR, "[role='radio']")
        
    print(f"Found {len(possible_radios)} potential radio buttons.")
    
    age_radios = []
    for r in possible_radios:
        # We assume these are the age radios
        age_radios.append(r)

    if not age_radios:
         raise Exception("No radios found for Age selection!")

    # Randomly select one age
    selected_age_radio = random.choice(age_radios)
    
    print("Clicking random age...")
    driver.execute_script("arguments[0].click();", selected_age_radio)
    time.sleep(1) # Wait for Biofach trigger
    
    # --- Biofach Question ---
    print("Looking for Biofach question (Ja/Yes)...")
    
    try:
        ja_xpath = "//label[.//span[text()='Ja' or text()='Yes']]//span[@data-automation-id='radio'] | //label[contains(., 'Ja') or contains(., 'Yes')]//span[@data-automation-id='radio']"
        
        ja_option = wait.until(EC.element_to_be_clickable((By.XPATH, ja_xpath)))
        driver.execute_script("arguments[0].click();", ja_option)
        print("Selected 'Ja' for Biofach.")
    except Exception as e:
        print(f"Could not find/click 'Ja' option: {e}")
        # Try finding by aria-label if applicable
        try:
            ja_option = driver.find_element(By.CSS_SELECTOR, "[aria-label='Ja'], [aria-label='Yes']")
            driver.execute_script("arguments[0].click();", ja_option)
            print("Selected 'Ja' by aria-label.")
        except:
            pass
    
    time.sleep(1)
    # Click Next
    next_btn_2 = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next'], button[aria-label='Weiter']")
    next_btn_2.click()
    print("Clicked Next (2)")
    
    # --- Screen 4: Startups ---
    # --- Screen 4: Startups ---
    print("Waiting for Startup checkboxes...")
    # Wait for checkboxes
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='checkbox']")))
    except:
        print("Timeout waiting for 'data-automation-id=checkbox', checking existence anyway...")
    
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "[data-automation-id='checkbox']")
    print(f"Found {len(checkboxes)} checkboxes.")
    
    aperitivo_checkbox = None
    other_checkboxes = []
    
    # The value from the screenshot is long, so we match a unique substring
    aperitivo_keyword = "Aperitivo Kollektiv"
    
    for cb in checkboxes:
        # data-automation-value contains the full text of the option
        val = cb.get_attribute("data-automation-value") or ""
        
        # Also check aria-label just in case
        lbl = cb.get_attribute("aria-label") or ""
        
        combined_text = (val + " " + lbl).lower()
        
        if aperitivo_keyword.lower() in combined_text:
            aperitivo_checkbox = cb
            print(f"Found Aperitivo checkbox via attribute: {val[:30]}...")
        else:
            other_checkboxes.append(cb)
    
    # Select Aperitivo
    if aperitivo_checkbox:
        print("Clicking Aperitivo...")
        # Scroll to it
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", aperitivo_checkbox)
        time.sleep(0.5)
        try:
            driver.execute_script("arguments[0].click();", aperitivo_checkbox)
        except:
             # Fallback standard click
             aperitivo_checkbox.click()
        time.sleep(0.5)
    else:
        print("CRITICAL WARNING: Could not find 'Aperitivo Kollektiv' checkbox!")
        # Optional: Dump all values found to help debugging
        print("Available options were:")
        for cb in checkboxes[:5]:
             print(f" - {cb.get_attribute('data-automation-value')}")

    # Select 2 random others
    print(f"Selecting 2 random others from {len(other_checkboxes)} candidates...")
    if len(other_checkboxes) >= 2:
        picks = random.sample(other_checkboxes, 2)
        for p in picks:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", p)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", p)
                time.sleep(0.3)
            except Exception as e:
                print(f"Failed to click random: {e}")
    else:
        print("Not enough other startups found!")

    time.sleep(1)
    next_btn_3 = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next'], button[aria-label='Weiter']")
    next_btn_3.click()
    print("Clicked Next (3)")
    
    # --- Screen 5: Submit ---
    print("Waiting for Submit button...")
    try:
         submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='submitButton']")))
         driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
         time.sleep(1)
         submit_btn.click()
         print("Clicked Submit!")
    except Exception as e:
         print(f"Submit button not found or clickable: {e}")
         print("Possible validation error on previous step? Capturing screenshot.")
         raise e
    
    time.sleep(5)

def main():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    options.add_argument("--start-maximized")
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        for i in range(NUM_SUBMISSIONS):
            print(f"\n==========================================")
            print(f"   {i+1} Turn")
            print(f"==========================================\n")
            
            try:
                submit_one_form(driver, wait)
                print(f"--- Submission {i+1} SUCCEEDED ---")
            except Exception as e:
                print(f"--- Submission {i+1} FAILED: {e} ---")
                driver.save_screenshot(f"error_run_{i+1}.png")
            
            # Small pause between iterations
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        print("Closing driver...")
        driver.quit()

if __name__ == "__main__":
    main()
