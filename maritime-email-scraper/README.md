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
