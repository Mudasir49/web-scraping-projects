# 🕷️ Web Scraping Projects

A collection of **professional web scraping scripts** built for real freelance clients.
All scripts were production-tested, processing thousands of URLs and records.

**Author:** Muhammad Mudasir Ahmad  
**GitHub:** [Mudasir49](https://github.com/Mudasir49)  
**LinkedIn:** [muhammad-mudasir-ahmad](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)  
**Email:** me.mudasirr@gmail.com

---

## 🛠️ Tools & Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-orange?style=flat-square)
![Azure Maps](https://img.shields.io/badge/Azure%20Maps%20API-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)
![Hunter.io](https://img.shields.io/badge/Hunter.io%20API-F55B50?style=flat-square)
![Excel](https://img.shields.io/badge/Excel%20%2F%20CSV-217346?style=flat-square&logo=microsoft-excel&logoColor=white)

---

## 📁 Projects (Best First)

| # | Project | Industry | Key Tech | Difficulty |
|---|---------|----------|----------|------------|
| 1 | [Tax Leads Pipeline](#1-tax-leads-pipeline) | Finance / US Business | Azure API + Hunter.io + Parallel | ⭐⭐⭐⭐⭐ |
| 2 | [Military Aerospace Scraper](#2-military-aerospace-scraper) | Defense | Playwright + Excel + Resume | ⭐⭐⭐⭐⭐ |
| 3 | [Aircraft Parts Scraper](#3-aircraft-parts-scraper) | Aviation | Selenium + Login + CDP | ⭐⭐⭐⭐ |
| 4 | [Aircraft Interiors Expo Scraper](#4-aircraft-interiors-expo-scraper) | Aviation | Selenium + JS Pages | ⭐⭐⭐ |
| 5 | [Maritime Email Scraper](#5-maritime-email-scraper) | Maritime | Selenium + CSV | ⭐⭐⭐ |
| 6 | [Community Centers Scraper](#6-community-centers-scraper) | Directory | Selenium + Multi-element | ⭐⭐ |
| 7 | [Exhibitor Link Scraper](#7-exhibitor-link-scraper) | Maritime | Selenium + Headless | ⭐⭐ |

---

## 1. Tax Leads Pipeline

**Industry:** Finance — Tax consultants across all 50 US states  
**Folder:** [`tax-leads-pipeline/`](./tax-leads-pipeline/)

A **2-script data pipeline** that first discovers businesses via Azure Maps API, then enriches each lead with contact data from their actual website and Hunter.io API.

**Script 1 — Generator:** 14 keywords × 200+ cities = 2,800+ searches, 5 parallel workers, live CSV  
**Script 2 — Enricher:** Scrapes company websites for emails, owner name, phone, social links

**Highlights:** Azure Maps API · Hunter.io API · Parallel threading · Resume support · Deduplication · Live ETA

---

## 2. Military Aerospace Scraper

**Industry:** Defense — Military & aerospace electronics directory  
**Folder:** [`military-aerospace-scraper/`](./military-aerospace-scraper/)

Scrapes company contact information from militaryaerospace.com with production-grade reliability features.

**Highlights:** Playwright · Formatted Excel output · Resume support · Retry with backoff · Regex email fallback · Bot detection bypass

---

## 3. Aircraft Parts Scraper

**Industry:** Aviation — Aircraft parts & supplies store  
**Folder:** [`aircraft-parts-scraper/`](./aircraft-parts-scraper/)

Scrapes product listings including prices and stock status after handling manual login and CAPTCHA.

**Highlights:** Manual login + CAPTCHA flow · CDP image blocking · Timeout recovery · Product price extraction

---

## 4. Aircraft Interiors Expo Scraper

**Industry:** Aviation — Trade show exhibitor directory  
**Folder:** [`aircraft-interiors-scraper/`](./aircraft-interiors-scraper/)

Handles JavaScript-rendered exhibitor pages with explicit waits and bot detection bypass.

**Highlights:** JS-rendered page handling · WebDriverWait · ExpectedConditions · Custom user-agent

---

## 5. Maritime Email Scraper

**Industry:** Maritime — Global maritime business directory  
**Folder:** [`maritime-email-scraper/`](./maritime-email-scraper/)

Extracts company names and emails from maritime company profiles with live CSV writing.

**Highlights:** CSS selector targeting · Live CSV writing · Production tested on 1000s of profiles

---

## 6. Community Centers Scraper

**Industry:** Directory — US community center listings  
**Folder:** [`community-centers-scraper/`](./community-centers-scraper/)

Extracts multiple listings per page including name, address, phone and website across all US states.

**Highlights:** Multi-element extraction per page · XPath + class selectors · Nationwide coverage

---

## 7. Exhibitor Link Scraper

**Industry:** Maritime — Trade show exhibitor directories  
**Folder:** [`exhibitor-link-scraper/`](./exhibitor-link-scraper/)

Extracts all external links from exhibitor profiles across two major maritime trade shows.

**Highlights:** Headless mode · Multi-site (seatrade + smm-hamburg) · Bulk URL processing

---

## ⚙️ General Setup

```bash
# Install all dependencies
pip install selenium webdriver-manager playwright beautifulsoup4 openpyxl requests lxml

# For Playwright only (script 2)
playwright install chromium
```

---

## 📊 Skills Demonstrated

- Selenium and Playwright browser automation
- Headless and visible browser modes
- JavaScript-rendered page handling
- Login, CAPTCHA, and session management
- REST API integration (Azure Maps, Hunter.io)
- Parallel/concurrent requests with ThreadPoolExecutor
- Resume and retry logic for production scrapers
- Data export to CSV and formatted Excel (.xlsx)
- Bot detection bypass (user-agent spoofing, resource blocking, CDP)
- Regex-based data extraction
- XPath and CSS selector targeting
- Multi-page pipeline architecture

---

## 📬 Contact & Freelance Work

Available for web scraping, data extraction, and automation projects.

📧 **me.mudasirr@gmail.com**  
💼 **[LinkedIn](https://www.linkedin.com/in/muhammad-mudasir-ahmad/)**