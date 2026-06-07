# 🏛️ Community Centers Directory Scraper
 
Scrapes community center listings from **lubavitch.com** across all US states and cities.
Built as a real paid freelance project delivering thousands of verified center records.
 
## 📦 Data Extracted
 
| Field | Description |
|-------|-------------|
| Name | Community center name |
| Address | Full street address |
| Phone Number | Contact phone |
| Website | Center website URL |
 
## ⚙️ How It Works
 
1. Runs Chrome headless with images disabled
2. Loops through state/city listing pages
3. Extracts multiple center listings per page using element loops
4. Uses both XPath and class-based selectors for robust extraction
5. Saves all data to `chabad_centers.csv`
## 🛠️ Tech Stack
Python · Selenium · WebDriverManager · XPath · CSS Selectors · CSV
 
## 🚀 Setup & Run
 
```bash
pip install selenium webdriver-manager
python community_centers_scraper.py
```
 
> Add your state/city URLs to the `urls` list before running.
 
## 💡 Key Features
- ✅ Handles multiple listings per page
- ✅ XPath + class selector targeting
- ✅ Headless + image-disabled for speed
- ✅ Production tested across all US states
## 📬 Contact
**Mudasir Ahmad** · me.mudasirr@gmail.com · [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
