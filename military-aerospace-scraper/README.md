# 🛡️ Military Aerospace Company Email Scraper

Scrapes company contact information from **militaryaerospace.com** — a leading directory of military and aerospace electronics companies.
Built as a real paid freelance project, processing thousands of company profiles in production.

## 📦 Data Extracted

| Field | Description |
|-------|-------------|
| Company Name | Full company name |
| Email | Contact email address |
| Status | OK / Error per URL |
| Source URL | Original company profile URL |

## ⚙️ How It Works

1. Launches headless Chromium via Playwright
2. Blocks images, fonts, and media for faster loading
3. Uses custom user-agent to avoid bot detection
4. Extracts company name and email from each profile page
5. Falls back to regex scan of full page body if mailto link not found
6. Retries up to 3 times with exponential backoff on failure
7. Saves results immediately to formatted Excel file
8. Resumes automatically from last saved row if interrupted

## 🛠️ Tech Stack

- Python
- Playwright
- openpyxl (formatted Excel output)
- Regular Expressions (regex fallback)

## 🚀 Setup & Run

```bash
pip install playwright openpyxl
playwright install chromium
python military_aerospace_scraper.py
```

> Add your company URLs to the `URLS` list in the script before running.

## 💡 Key Features

- ✅ Resume support — never loses progress if interrupted
- ✅ Retry logic — 3 attempts per URL with backoff
- ✅ Regex fallback email extraction from page body
- ✅ Beautifully formatted Excel output (color-coded, hyperlinks, summary row)
- ✅ Resource blocking for speed and stealth
- ✅ Custom user-agent for bot detection bypass
- ✅ Production tested on thousands of company URLs

## 📊 Excel Output Format

- Color-coded header row (dark blue)
- Alternating row colors for readability
- Green text for found emails, red for errors
- Clickable hyperlinks in Source URL column
- Summary row at bottom with totals

## 📬 Contact

**Muhammad Mudasir Ahmad**
📧 me.mudasirr@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
