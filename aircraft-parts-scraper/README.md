# ✈️ Aircraft Parts Scraper

Scrapes product listings from **aircraftspruce.com** — a major aviation parts and supplies store.
Built as a real paid freelance project, processing hundreds of product URLs in production.

## 📦 Data Extracted

| Field | Description |
|-------|-------------|
| Product Name | Full product title |
| Overview | Product description text |
| Part # | Manufacturer part number |
| MFR Model # | Manufacturer model number |
| Image Link | Direct URL to product image |
| Regular Price | Standard listed price |
| Net Price | Discounted/net price |
| Stock Status | In stock / out of stock |
| Source URL | Original product page URL |

## ⚙️ How It Works

1. Opens Chrome browser for manual login + CAPTCHA solving
2. After login confirmed, blocks all images via Chrome DevTools Protocol (CDP) for faster scraping
3. Loops through all product URLs, extracts data
4. Handles timeouts gracefully — writes error placeholder and continues
5. Saves everything to `AirCraft.csv`

## 🛠️ Tech Stack

- Python
- Selenium
- WebDriverManager
- Chrome DevTools Protocol (CDP)
- CSV

## 🚀 Setup & Run

```bash
pip install selenium webdriver-manager
python aircraft_scraper.py
```

> Add your product URLs to the `PRODUCT_URLS` list in the script before running.

## 💡 Key Features

- ✅ Manual login + CAPTCHA support
- ✅ CDP image blocking for speed
- ✅ Timeout error handling — never crashes mid-run
- ✅ Immediate CSV flush after each product
- ✅ Production tested on hundreds of URLs

## 📬 Contact

**Mudasir Ahmad**
📧 me.mudasirr@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
