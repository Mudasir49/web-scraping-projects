# 💼 Tax Leads Pipeline

A **2-script data pipeline** that discovers and enriches business leads for tax consultants across all 50 US states.

Built as a real paid freelance project delivering thousands of verified, enriched business contacts.

---

## 🗂️ Pipeline Overview

```
Script 1 — tax_leads_generator.py
    └── Azure Maps API
    └── 14 keywords × 200+ US cities
    └── Output: tax_leads_results.csv
            │
            ▼
Script 2 — tax_leads_enricher.py
    └── Visits each company website
    └── Hunter.io API fallback
    └── Output: tax_leads_enriched.csv
```

---

## 📦 Data Extracted

### Script 1 — Generator Output
| Field | Description |
|-------|-------------|
| Company Name | Business name |
| Full Address | Complete address |
| City / State / Zip | Location |
| Phone | Business phone |
| Website | Business website |
| Business Category | Type of business |
| Search Keyword | Keyword used |
| Bing Maps Link | Direct map link |
| Google Search Link | Pre-built search |
| Date Collected | Collection date |

### Script 2 — Enricher Output (adds to above)
| Field | Description |
|-------|-------------|
| Company Email | General contact email |
| Owner Name | Business owner name |
| Owner Phone | Owner direct phone |
| Owner Email | Owner personal email |
| Facebook Page | Company Facebook URL |
| YouTube Channel | Company YouTube URL |
| Enrichment Source | Where data was found |

---

## ⚙️ How It Works

### Script 1 — Tax Leads Generator
1. Loops through 14 tax-related keywords across 200+ US cities
2. Fires **5 parallel API requests** at the same time (5x speed)
3. Deduplicates results by company name + state
4. Shows live ETA while running
5. Saves to CSV live — open file anytime during run
6. Resumes automatically if interrupted

### Script 2 — Tax Leads Enricher
1. Reads the CSV from Script 1
2. Visits each company's website (up to 8 pages per site)
3. Extracts emails, owner names, phones using regex + BeautifulSoup
4. Falls back to **Hunter.io API** if website scraping finds nothing
5. Falls back to Facebook/YouTube links if no email found at all
6. Matches owner email to owner name automatically
7. Runs **5 parallel workers** for speed
8. Saves enriched data to new CSV live while running
9. Resumes from last saved row if interrupted

---

## 🛠️ Tech Stack

| Tool | Used For |
|------|---------|
| Azure Maps API | Discovering businesses by keyword + location |
| Hunter.io API | Email lookup by company domain |
| requests | HTTP requests and API calls |
| BeautifulSoup | HTML parsing for email/owner extraction |
| ThreadPoolExecutor | Parallel requests (5x speed) |
| openpyxl | Reading input Excel file |
| CSV | Live output writing |
| Regex | Email, phone, owner name extraction |

---

## 🚀 Setup & Run

```bash
pip install requests beautifulsoup4 openpyxl lxml
```

### Run Script 1 First:
```bash
python 1_tax_leads_generator.py
```
- Add your `AZURE_MAPS_API_KEY` in the config section
- Output: `tax_leads_results.csv`

### Then Run Script 2:
```bash
python 2_tax_leads_enricher.py
```
- Add your `HUNTER_API_KEY` in the config section
- Make sure `tax_leads_results.xlsx` exists from Script 1
- Output: `tax_leads_enriched.csv`

---

## 📊 Scale

| Metric | Value |
|--------|-------|
| Search keywords | 14 tax-related terms |
| Cities covered | 200+ across all 50 US states |
| Total API searches | 2,800+ queries |
| Parallel workers | 5 simultaneous |
| Pages scraped per company | Up to 8 (home, contact, about, team...) |

---

## 💡 Key Features

- ✅ 2-script pipeline architecture (discover → enrich)
- ✅ Azure Maps API for nationwide business discovery
- ✅ Hunter.io API fallback for hard-to-find emails
- ✅ 5x parallel speed in both scripts
- ✅ Resume support in both scripts — never loses progress
- ✅ Live CSV writing — open output file anytime
- ✅ Live ETA display during run
- ✅ Smart deduplication
- ✅ Owner name matching to owner email
- ✅ Social media fallback when no email found

---

## 📬 Contact

**Muhammad Mudasir Ahmad**  
📧 me.mudasirr@gmail.com  
💼 [LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)
