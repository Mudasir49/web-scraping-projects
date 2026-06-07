"""
==============================================================
  TAX LEADS SCRAPER v2 FAST — Azure Maps API
  City-by-City + Parallel Requests
  
  Improvements over v2:
  - 5 parallel requests (5x faster)
  - CSV live save (no Excel lock issues)
  - 10s timeout (safe balance)
  - Live ETA display
  - Small radius per city (more accurate results)
  - Resume support
==============================================================

HOW TO RUN:
1. pip install requests
2. python tax_leads_scraper_v2_fast.py
3. Open tax_leads_results.csv anytime while running
==============================================================
"""

import requests
import time
import datetime
import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
AZURE_MAPS_KEY    = "YOUR_AZURE_MAPS_API_KEY_HERE"
OUTPUT_FILE       = "tax_leads_results.csv"
RESULTS_PER_QUERY = 100
PARALLEL_WORKERS  = 5    # 5 requests at same time
TIMEOUT           = 10   # 10s — safe balance (5s too aggressive)
CITY_RADIUS       = 30000  # 30km per city — tight, accurate, no overlap
# ============================================================

KEYWORDS = [
    "Tax Strategist", "Tax Advisor", "Tax Consultant",
    "Creative Tax Planning", "Tax Planning Specialist",
    "Tax Planning Advisor", "Tax Optimization Specialist",
    "Tax Strategy Consultant", "Tax Planning Expert",
    "Strategic Tax Advisor", "Tax Efficiency Consultant",
    "Wealth Tax Strategist", "Tax Advisory Specialist",
    "Tax Management Consultant"
]

# Cities proportional to business density
# Big states (CA, TX, NY, FL) get more cities
# Small states get fewer
US_CITIES = [

    # Alabama
    ("Birmingham", "Alabama", 33.5186, -86.8104),
    ("Montgomery", "Alabama", 32.3668, -86.3000),
    ("Huntsville", "Alabama", 34.7304, -86.5861),
    ("Mobile", "Alabama", 30.6954, -88.0399),
    # Alaska
    ("Anchorage", "Alaska", 61.2181, -149.9003),
    ("Fairbanks", "Alaska", 64.8378, -147.7164),
    # Arizona
    ("Phoenix", "Arizona", 33.4484, -112.0740),
    ("Tucson", "Arizona", 32.2226, -110.9747),
    ("Scottsdale", "Arizona", 33.4942, -111.9261),
    ("Mesa", "Arizona", 33.4152, -111.8315),
    ("Chandler", "Arizona", 33.3062, -111.8413),
    ("Tempe", "Arizona", 33.4255, -111.9400),
    # Arkansas
    ("Little Rock", "Arkansas", 34.7465, -92.2896),
    ("Fayetteville", "Arkansas", 36.0626, -94.1574),
    ("Fort Smith", "Arkansas", 35.3859, -94.3985),
    # California
    ("Los Angeles", "California", 34.0522, -118.2437),
    ("San Francisco", "California", 37.7749, -122.4194),
    ("San Diego", "California", 32.7157, -117.1611),
    ("Sacramento", "California", 38.5816, -121.4944),
    ("San Jose", "California", 37.3382, -121.8863),
    ("Fresno", "California", 36.7378, -119.7871),
    ("Oakland", "California", 37.8044, -122.2712),
    ("Long Beach", "California", 33.7701, -118.1937),
    ("Bakersfield", "California", 35.3733, -119.0187),
    ("Anaheim", "California", 33.8366, -117.9143),
    ("Santa Ana", "California", 33.7455, -117.8677),
    ("Irvine", "California", 33.6846, -117.8265),
    ("Beverly Hills", "California", 34.0736, -118.4004),
    ("Pasadena", "California", 34.1478, -118.1445),
    ("Newport Beach", "California", 33.6189, -117.9289),
    # Colorado
    ("Denver", "Colorado", 39.7392, -104.9903),
    ("Colorado Springs", "Colorado", 38.8339, -104.8214),
    ("Boulder", "Colorado", 40.0150, -105.2705),
    ("Aurora", "Colorado", 39.7294, -104.8319),
    ("Fort Collins", "Colorado", 40.5853, -105.0844),
    # Connecticut
    ("Hartford", "Connecticut", 41.7658, -72.6851),
    ("New Haven", "Connecticut", 41.3083, -72.9279),
    ("Stamford", "Connecticut", 41.0534, -73.5387),
    ("Bridgeport", "Connecticut", 41.1865, -73.1952),
    # Delaware
    ("Wilmington", "Delaware", 39.7447, -75.5484),
    ("Dover", "Delaware", 39.1582, -75.5244),
    # Florida
    ("Miami", "Florida", 25.7617, -80.1918),
    ("Orlando", "Florida", 28.5383, -81.3792),
    ("Tampa", "Florida", 27.9506, -82.4572),
    ("Jacksonville", "Florida", 30.3322, -81.6557),
    ("Fort Lauderdale", "Florida", 26.1224, -80.1373),
    ("St. Petersburg", "Florida", 27.7676, -82.6403),
    ("Boca Raton", "Florida", 26.3683, -80.1289),
    ("Naples", "Florida", 26.1420, -81.7948),
    ("Sarasota", "Florida", 27.3364, -82.5307),
    ("West Palm Beach", "Florida", 26.7153, -80.0534),
    # Georgia
    ("Atlanta", "Georgia", 33.7490, -84.3880),
    ("Savannah", "Georgia", 32.0835, -81.0998),
    ("Augusta", "Georgia", 33.4735, -82.0105),
    ("Columbus", "Georgia", 32.4610, -84.9877),
    ("Alpharetta", "Georgia", 34.0754, -84.2941),
    # Hawaii
    ("Honolulu", "Hawaii", 21.3069, -157.8583),
    # Idaho
    ("Boise", "Idaho", 43.6150, -116.2023),
    ("Nampa", "Idaho", 43.5407, -116.5635),
    # Illinois
    ("Chicago", "Illinois", 41.8781, -87.6298),
    ("Springfield", "Illinois", 39.7817, -89.6501),
    ("Naperville", "Illinois", 41.7508, -88.1535),
    ("Rockford", "Illinois", 42.2711, -89.0940),
    ("Peoria", "Illinois", 40.6936, -89.5890),
    ("Schaumburg", "Illinois", 42.0334, -88.0834),
    # Indiana
    ("Indianapolis", "Indiana", 39.7684, -86.1581),
    ("Fort Wayne", "Indiana", 41.1306, -85.1289),
    ("Evansville", "Indiana", 37.9716, -87.5711),
    ("South Bend", "Indiana", 41.6764, -86.2520),
    # Iowa
    ("Des Moines", "Iowa", 41.5868, -93.6250),
    ("Cedar Rapids", "Iowa", 41.9779, -91.6656),
    ("Davenport", "Iowa", 41.5236, -90.5776),
    # Kansas (3)
    ("Wichita",         "Kansas",     37.6872,  -97.3301),
    ("Overland Park",   "Kansas",     38.9822,  -94.6708),
    ("Kansas City",     "Kansas",     39.1155,  -94.6268),
    # Kentucky (3)
    ("Louisville",      "Kentucky",   38.2527,  -85.7585),
    ("Lexington",       "Kentucky",   38.0406,  -84.5037),
    ("Bowling Green",   "Kentucky",   36.9685,  -86.4808),
    # Louisiana (3)
    ("New Orleans",     "Louisiana",  29.9511,  -90.0715),
    ("Baton Rouge",     "Louisiana",  30.4515,  -91.1871),
    ("Shreveport",      "Louisiana",  32.5252,  -93.7502),
    # Maine (2)
    ("Portland",        "Maine",      43.6591,  -70.2568),
    ("Bangor",          "Maine",      44.8016,  -68.7712),
    # Maryland (4)
    ("Baltimore",       "Maryland",   39.2904,  -76.6122),
    ("Rockville",       "Maryland",   39.0840,  -77.1528),
    ("Annapolis",       "Maryland",   38.9784,  -76.4922),
    ("Bethesda",        "Maryland",   38.9807,  -77.1003),
    # Massachusetts (5)
    ("Boston",          "Massachusetts",42.3601, -71.0589),
    ("Worcester",       "Massachusetts",42.2626, -71.8023),
    ("Springfield",     "Massachusetts",42.1015, -72.5898),
    ("Cambridge",       "Massachusetts",42.3736, -71.1097),
    ("Newton",          "Massachusetts",42.3370, -71.2092),
    # Michigan (5)
    ("Detroit",         "Michigan",   42.3314,  -83.0458),
    ("Grand Rapids",    "Michigan",   42.9634,  -85.6681),
    ("Ann Arbor",       "Michigan",   42.2808,  -83.7430),
    ("Lansing",         "Michigan",   42.7325,  -84.5555),
    ("Troy",            "Michigan",   42.6064,  -83.1498),
    # Minnesota (4)
    ("Minneapolis",     "Minnesota",  44.9778,  -93.2650),
    ("Saint Paul",      "Minnesota",  44.9537,  -93.0900),
    ("Rochester",       "Minnesota",  44.0121,  -92.4802),
    ("Bloomington",     "Minnesota",  44.8408,  -93.3477),
    # Mississippi (2)
    ("Jackson",         "Mississippi",32.2988,  -90.1848),
    ("Gulfport",        "Mississippi",30.3674,  -89.0928),
    # Missouri (4)
    ("Kansas City",     "Missouri",   39.0997,  -94.5786),
    ("St. Louis",       "Missouri",   38.6270,  -90.1994),
    ("Springfield",     "Missouri",   37.2090,  -93.2923),
    ("Columbia",        "Missouri",   38.9517,  -92.3341),
    # Montana (2)
    ("Billings",        "Montana",    45.7833, -108.5007),
    ("Missoula",        "Montana",    46.8721, -113.9940),
    # Nebraska (2)
    ("Omaha",           "Nebraska",   41.2565,  -95.9345),
    ("Lincoln",         "Nebraska",   40.8136,  -96.7026),
    # Nevada (4)
    ("Las Vegas",       "Nevada",     36.1699, -115.1398),
    ("Henderson",       "Nevada",     36.0397, -114.9817),
    ("Reno",            "Nevada",     39.5296, -119.8138),
    ("Carson City",     "Nevada",     39.1638, -119.7674),
    # New Hampshire (2)
    ("Manchester",      "New Hampshire",42.9956, -71.4548),
    ("Nashua",          "New Hampshire",42.7654, -71.4676),
    # New Jersey (6)
    ("Newark",          "New Jersey", 40.7357,  -74.1724),
    ("Jersey City",     "New Jersey", 40.7178,  -74.0431),
    ("Trenton",         "New Jersey", 40.2171,  -74.7429),
    ("Edison",          "New Jersey", 40.5187,  -74.4121),
    ("Parsippany",      "New Jersey", 40.8576,  -74.4254),
    ("Cherry Hill",     "New Jersey", 39.9348,  -74.9985),
    # New Mexico (2)
    ("Albuquerque",     "New Mexico", 35.0844, -106.6504),
    ("Santa Fe",        "New Mexico", 35.6870, -105.9378),
    # New York (10)
    ("New York City",   "New York",   40.7128,  -74.0060),
    ("Buffalo",         "New York",   42.8864,  -78.8784),
    ("Rochester",       "New York",   43.1566,  -77.6088),
    ("Albany",          "New York",   42.6526,  -73.7562),
    ("Syracuse",        "New York",   43.0481,  -76.1474),
    ("White Plains",    "New York",   41.0340,  -73.7629),
    ("Yonkers",         "New York",   40.9312,  -73.8988),
    ("Manhattan",       "New York",   40.7831,  -73.9712),
    ("Brooklyn",        "New York",   40.6782,  -73.9442),
    ("Long Island City","New York",   40.7447,  -73.9485),
    # North Carolina (6)
    ("Charlotte",       "North Carolina",35.2271,-80.8431),
    ("Raleigh",         "North Carolina",35.7796,-78.6382),
    ("Greensboro",      "North Carolina",36.0726,-79.7920),
    ("Durham",          "North Carolina",35.9940,-78.8986),
    ("Winston-Salem",   "North Carolina",36.0999,-80.2442),
    ("Asheville",       "North Carolina",35.5951,-82.5515),
    # North Dakota (2)
    ("Fargo",           "North Dakota",46.8772, -96.7898),
    ("Bismarck",        "North Dakota",46.8083,-100.7837),
    # Ohio (6)
    ("Columbus",        "Ohio",       39.9612,  -82.9988),
    ("Cleveland",       "Ohio",       41.4993,  -81.6944),
    ("Cincinnati",      "Ohio",       39.1031,  -84.5120),
    ("Toledo",          "Ohio",       41.6528,  -83.5379),
    ("Akron",           "Ohio",       41.0814,  -81.5190),
    ("Dayton",          "Ohio",       39.7589,  -84.1916),
    # Oklahoma (2)
    ("Oklahoma City",   "Oklahoma",   35.4676,  -97.5164),
    ("Tulsa",           "Oklahoma",   36.1540,  -95.9928),
    # Oregon (4)
    ("Portland",        "Oregon",     45.5051, -122.6750),
    ("Eugene",          "Oregon",     44.0521, -123.0868),
    ("Salem",           "Oregon",     44.9429, -123.0351),
    ("Bend",            "Oregon",     44.0582, -121.3153),
    # Pennsylvania (6)
    ("Philadelphia",    "Pennsylvania",39.9526, -75.1652),
    ("Pittsburgh",      "Pennsylvania",40.4406, -79.9959),
    ("Allentown",       "Pennsylvania",40.6084, -75.4902),
    ("Erie",            "Pennsylvania",42.1292, -80.0851),
    ("King of Prussia", "Pennsylvania",40.0913, -75.3824),
    ("Harrisburg",      "Pennsylvania",40.2732, -76.8867),
    # Rhode Island (1)
    ("Providence",      "Rhode Island",41.8240, -71.4128),
    # South Carolina (3)
    ("Columbia",        "South Carolina",34.0007,-81.0348),
    ("Charleston",      "South Carolina",32.7765,-79.9311),
    ("Greenville",      "South Carolina",34.8526,-82.3940),
    # South Dakota (2)
    ("Sioux Falls",     "South Dakota",43.5446, -96.7311),
    ("Rapid City",      "South Dakota",44.0805,-103.2310),
    # Tennessee (4)
    ("Nashville",       "Tennessee",  36.1627,  -86.7816),
    ("Memphis",         "Tennessee",  35.1495,  -90.0490),
    ("Knoxville",       "Tennessee",  35.9606,  -83.9207),
    ("Chattanooga",     "Tennessee",  35.0456,  -85.3097),
    # Texas (13)
    ("Houston",         "Texas",      29.7604,  -95.3698),
    ("Dallas",          "Texas",      32.7767,  -96.7970),
    ("Austin",          "Texas",      30.2672,  -97.7431),
    ("San Antonio",     "Texas",      29.4241,  -98.4936),
    ("Fort Worth",      "Texas",      32.7555,  -97.3308),
    ("El Paso",         "Texas",      31.7619, -106.4850),
    ("Plano",           "Texas",      33.0198,  -96.6989),
    ("Irving",          "Texas",      32.8140,  -96.9489),
    ("Arlington",       "Texas",      32.7357,  -97.1081),
    ("Frisco",          "Texas",      33.1507,  -96.8236),
    ("The Woodlands",   "Texas",      30.1658,  -95.5046),
    ("Sugar Land",      "Texas",      29.6197,  -95.6349),
    ("Lubbock",         "Texas",      33.5779, -101.8552),
    # Utah (4)
    ("Salt Lake City",  "Utah",       40.7608, -111.8910),
    ("Provo",           "Utah",       40.2338, -111.6585),
    ("Sandy",           "Utah",       40.5649, -111.8389),
    ("St. George",      "Utah",       37.0965, -113.5684),
    # Vermont (1)
    ("Burlington",      "Vermont",    44.4759,  -73.2121),
    # Virginia (7)
    ("Virginia Beach",  "Virginia",   36.8529,  -75.9780),
    ("Norfolk",         "Virginia",   36.8508,  -76.2859),
    ("Richmond",        "Virginia",   37.5407,  -77.4360),
    ("Arlington",       "Virginia",   38.8816,  -77.0910),
    ("Alexandria",      "Virginia",   38.8048,  -77.0469),
    ("McLean",          "Virginia",   38.9339,  -77.1773),
    ("Reston",          "Virginia",   38.9586,  -77.3570),
    # Washington (5)
    ("Seattle",         "Washington", 47.6062, -122.3321),
    ("Spokane",         "Washington", 47.6588, -117.4260),
    ("Tacoma",          "Washington", 47.2529, -122.4443),
    ("Bellevue",        "Washington", 47.6101, -122.2015),
    ("Redmond",         "Washington", 47.6740, -122.1215),
    # West Virginia (2)
    ("Charleston",      "West Virginia",38.3498,-81.6326),
    ("Huntington",      "West Virginia",38.4193,-82.4452),
    # Wisconsin (3)
    ("Milwaukee",       "Wisconsin",  43.0389,  -87.9065),
    ("Madison",         "Wisconsin",  43.0731,  -89.4012),
    ("Green Bay",       "Wisconsin",  44.5133,  -88.0133),
    # Wyoming (2)
    ("Cheyenne",        "Wyoming",    41.1400, -104.8202),
    ("Casper",          "Wyoming",    42.8501, -106.3252),
]

CSV_HEADERS = [
    "Company Name", "Full Address", "City", "State", "State Code",
    "Zip Code", "Phone", "Website", "Business Category",
    "Search Keyword", "Search City", "Search State",
    "Bing Maps Link", "Google Search Link", "API Source Link",
    "Date Collected"
]


# ============================================================
#   SINGLE SEARCH — runs in parallel
# ============================================================

def search_one(keyword, city, state, lat, lon):
    query = f"{keyword} {city} {state}"
    try:
        response = requests.get(
            "https://atlas.microsoft.com/search/poi/json",
            params={
                "api-version":      "1.0",
                "subscription-key": AZURE_MAPS_KEY,
                "query":            query,
                "countrySet":       "US",
                "lat":              lat,
                "lon":              lon,
                "radius":           CITY_RADIUS,
                "limit":            RESULTS_PER_QUERY,
                "language":         "en-US"
            },
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            results = []
            for item in response.json().get("results", []):
                poi     = item.get("poi", {})
                address = item.get("address", {})
                name    = poi.get("name", "")
                if not name:
                    continue

                city_found = address.get("municipality", "")
                bing   = f"https://www.bing.com/maps?q={name.replace(' ', '+')}+{city_found.replace(' ', '+')}"
                google = f"https://www.google.com/search?q={name.replace(' ', '+')}+{keyword.replace(' ', '+')}+{city.replace(' ', '+')}"
                api    = f"https://atlas.microsoft.com/search/poi/json?query={query.replace(' ', '+')}&countrySet=US"

                results.append({
                    "Company Name":       name,
                    "Full Address":       address.get("freeformAddress", ""),
                    "City":               city_found,
                    "State":              state,
                    "State Code":         address.get("countrySubdivision", ""),
                    "Zip Code":           address.get("postalCode", ""),
                    "Phone":              poi.get("phone", ""),
                    "Website":            poi.get("url", ""),
                    "Business Category":  ", ".join(poi.get("categories", [])),
                    "Search Keyword":     keyword,
                    "Search City":        city,
                    "Search State":       state,
                    "Bing Maps Link":     bing,
                    "Google Search Link": google,
                    "API Source Link":    api,
                    "Date Collected":     datetime.datetime.now().strftime("%Y-%m-%d")
                })
            return keyword, city, state, results
        else:
            return keyword, city, state, []
    except:
        return keyword, city, state, []


# ============================================================
#   RESUME SUPPORT
# ============================================================

def load_done_and_seen():
    done_searches  = set()
    seen_companies = set()
    total_saved    = 0
    if not os.path.exists(OUTPUT_FILE):
        return done_searches, seen_companies, 0
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kw   = row.get("Search Keyword", "").strip()
                city = row.get("Search City",    "").strip()
                name = row.get("Company Name",   "").strip().lower()
                st   = row.get("State",          "").strip().lower()
                if kw and city:
                    done_searches.add((kw, city))
                if name and st:
                    seen_companies.add((name, st))
                total_saved += 1
    except:
        pass
    return done_searches, seen_companies, total_saved


# ============================================================
#   MAIN
# ============================================================

def main():
    total_queries = len(US_CITIES) * len(KEYWORDS)

    print("=" * 65)
    print("   TAX LEADS SCRAPER v2 FAST — City by City + Parallel")
    print(f"   {PARALLEL_WORKERS} parallel | {TIMEOUT}s timeout | {CITY_RADIUS//1000}km radius")
    print("=" * 65)
    print(f"\n  Cities   : {len(US_CITIES)}")
    print(f"  Keywords : {len(KEYWORDS)}")
    print(f"  Searches : {total_queries}")
    print(f"  Output   : {OUTPUT_FILE}")

    done_searches, seen_companies, total_saved = load_done_and_seen()
    if done_searches:
        print(f"\n  ♻️  Resuming — {len(done_searches)} done, {total_saved} saved")

    # Build pending tasks
    all_tasks = [
        (kw, city, state, lat, lon)
        for (city, state, lat, lon) in US_CITIES
        for kw in KEYWORDS
        if (kw, city) not in done_searches
    ]

    pending = len(all_tasks)
    print(f"  Pending  : {pending} searches remaining")
    print(f"\n  Open {OUTPUT_FILE} anytime — updates live!\n")

    if pending == 0:
        print("  ✅ All searches already done!")
        return

    file_exists = os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0
    completed   = 0
    new_saved   = 0
    start_time  = time.time()

    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
            csvfile.flush()

        for i in range(0, len(all_tasks), PARALLEL_WORKERS):
            batch = all_tasks[i:i + PARALLEL_WORKERS]

            with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
                futures = {
                    executor.submit(search_one, kw, city, state, lat, lon): (kw, city)
                    for kw, city, state, lat, lon in batch
                }

                for future in as_completed(futures):
                    keyword, city, state, results = future.result()
                    completed += 1

                    # Deduplicate
                    unique_new = []
                    for r in results:
                        key = (r["Company Name"].lower().strip(), r["State"].lower().strip())
                        if key not in seen_companies:
                            seen_companies.add(key)
                            unique_new.append(r)

                    # Save immediately to CSV
                    for r in unique_new:
                        writer.writerow({h: r.get(h, "") for h in CSV_HEADERS})
                    if unique_new:
                        csvfile.flush()
                        new_saved   += len(unique_new)
                        total_saved += len(unique_new)

                    # ETA
                    elapsed  = time.time() - start_time
                    speed    = completed / elapsed if elapsed > 0 else 1
                    eta_min  = (pending - completed) / speed / 60 if speed > 0 else 0

                    print(
                        f"  [{completed:>4}/{pending}] "
                        f"{keyword[:25]:<25} {city:<18} {state:<15} "
                        f"✓{len(unique_new):>3} new | "
                        f"total:{total_saved:>5} | "
                        f"ETA:{eta_min:>5.1f}min"
                    )

    elapsed_total = (time.time() - start_time) / 60
    print(f"\n{'=' * 65}")
    print(f"  COMPLETE!")
    print(f"  New companies : {new_saved}")
    print(f"  Total in file : {total_saved}")
    print(f"  Time taken    : {elapsed_total:.1f} minutes")
    print(f"  Output        : {OUTPUT_FILE}")
    print(f"{'=' * 65}\n")


if __name__ == "__main__":
    main()