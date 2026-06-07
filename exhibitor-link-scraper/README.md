# 🚢 Exhibitor Link Scraper
 
Scrapes exhibitor profile pages from **seatrade-europe.com** and **smm-hamburg.com** — two of the world's largest maritime trade show directories.
Built as a real paid freelance project, processing thousands of exhibitor URLs in production.
 
## 📦 Data Extracted
 
| Field | Description |
|-------|-------------|
| External Links | All website and social media links per exhibitor |
| Source URL | Original exhibitor profile page |
 
## ⚙️ How It Works
 
1. Runs Chrome fully headless — no browser window, silent execution
2. Disables images for faster loading
3. Loops through exhibitor profile URLs
4. Extracts all anchor tags from the links section
5. Prints all href links for each exhibitor
## 🛠️ Tech Stack
Python · Selenium · WebDriverManager · CSS Selectors · Headless Chrome
 
## 🚀 Setup & Run
 
```bash
pip install selenium webdriver-manager
python exhibitor_link_scraper.py
```
 
> Add your exhibitor profile URLs to the `urls` list before running.
 
## 💡 Key Features
- ✅ Fully headless — runs silently in background
- ✅ Image blocking for faster loading
- ✅ Multi-site (seatrade + smm-hamburg)
- ✅ Production tested on thousands of URLs
## 📬 Contact
**Mudasir Ahmad** · me.mudasirr@gmail.com · [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
