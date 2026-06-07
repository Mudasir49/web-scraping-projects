# 🛩️ Aircraft Interiors Expo Scraper
 
Scrapes exhibitor profiles from **aircraftinteriorsexpo.com** — one of the world's largest aviation interiors trade shows.
Built as a real paid freelance project, processing thousands of exhibitor profiles in production.
 
## 📦 Data Extracted
 
| Field | Description |
|-------|-------------|
| Company Name | Full exhibitor company name |
| Email | Contact email address |
| Source URL | Original exhibitor profile URL |
 
## ⚙️ How It Works
 
1. Runs Chrome with custom user-agent to avoid bot detection
2. Uses WebDriverWait + ExpectedConditions to handle JS-rendered pages
3. Waits for company name element to fully load before extracting
4. Extracts email from mailto link in contact section
5. Saves all data to `aix_companies_data.csv`
## 🛠️ Tech Stack
Python · Selenium · WebDriverWait · ExpectedConditions · WebDriverManager · CSV
 
## 🚀 Setup & Run
 
```bash
pip install selenium webdriver-manager
python aircraft_interiors_scraper.py
```
 
> Add your exhibitor URLs to the `urls` list before running.
 
## 💡 Key Features
- ✅ JavaScript-rendered page handling with explicit waits
- ✅ Custom user-agent for bot detection bypass
- ✅ ExpectedConditions — no random crashes from timing
- ✅ Production tested on thousands of exhibitor URLs
## 📬 Contact
**Muhammad Mudasir Ahmad** · me.mudasirr@gmail.com · [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
 
---
---
---
 
# ⚓ Maritime Company Email Scraper
 
Scrapes company contact information from **yourmaritime.com** — a global maritime industry business directory.
Built as a real paid freelance project, processing thousands of company profiles in production.
 
## 📦 Data Extracted
 
| Field | Description |
|-------|-------------|
| Company Name | Full company name |
| Email | Contact email address |
| Source URL | Original profile URL |
 
## ⚙️ How It Works
 
1. Runs Chrome headless with images disabled for speed
2. Loops through company profile URLs
3. Extracts company name via CSS selector targeting
4. Extracts email from mailto link
5. Writes each row to CSV immediately — no data loss
## 🛠️ Tech Stack
Python · Selenium · WebDriverManager · CSS Selectors · CSV
 
## 🚀 Setup & Run
 
```bash
pip install selenium webdriver-manager
python maritime_email_scraper.py
```
 
> Add your company URLs to the `urls` list before running.
 
## 💡 Key Features
- ✅ Live CSV writing — safe if interrupted
- ✅ Headless + image-disabled for speed
- ✅ Production tested on thousands of company profiles
## 📬 Contact
**Mudasir Ahmad** · me.mudasirr@gmail.com · [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
