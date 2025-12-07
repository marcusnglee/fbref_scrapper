# FBref Player Stats Scraper - Complete Guide

A Python tool to scrape player statistics from FBref.com, with smart player URL discovery from transfer data.

## Quick Start (3 Steps)

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Get player URLs**: `python3 get_player_urls_from_csv.py`
3. **Scrape player stats**: `python3 scrape_multiple_players.py`

---

## What This Tool Does

This scraper helps you:
1. Extract all unique player names from a CSV file (like transfer data)
2. Find their FBref profile URLs automatically
3. Scrape detailed statistics for each player

**Key Features:**
- ✅ Bypasses Cloudflare protection using cloudscraper
- ✅ Smart mode: Only scrapes needed pages (saves 70% of time)
- ✅ Automatic checkpointing (resume if interrupted)
- ✅ Respectful rate limiting
- ✅ Exports to CSV/JSON

---

## Installation

### 1. Clone or Download Repository

Download this folder to your machine (or school lab computer).

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- pandas
- cloudscraper
- beautifulsoup4
- requests

### 3. Prepare Your Data

Place your CSV file with player names in the project folder. Default filename: `transfers_1.csv`

**CSV Requirements:**
- Must have a column named `Player` with player names
- Example: `Fernando Torres`, `Cristiano Ronaldo`, etc.

---

## Step 1: Get Player URLs from CSV

This step discovers FBref URLs for all unique players in your CSV.

### Run the Smart URL Finder

```bash
python3 get_player_urls_from_csv.py
```

### What It Does

1. **Extracts unique players** from your CSV (e.g., 2,529 unique names)
2. **Analyzes which letter combinations are needed** (e.g., "aa", "cr", "me", etc.)
3. **Scrapes only required pages** from FBref's player index (192 pages instead of 676)
4. **Matches players** to their URLs using fuzzy matching (handles accents, case differences)
5. **Saves results** to JSON file

### Expected Runtime

- **Smart mode**: ~20-30 minutes (depends on delay setting)
- **Pages scraped**: ~190-200 (instead of 676)
- **Default delay**: 8 seconds between requests (avoids rate limits)

### Options

```bash
# Use custom CSV file
python3 get_player_urls_from_csv.py --csv your_file.csv

# Adjust delay (increase if getting rate limited)
python3 get_player_urls_from_csv.py --delay 10

# Start fresh (ignore checkpoint)
python3 get_player_urls_from_csv.py --no-resume
```

### Output Files

After completion, you'll get:

1. **`player_urls.json`** - Matched players with their FBref URLs
   ```json
   {
     "Cristiano Ronaldo": "https://fbref.com/en/players/.../Cristiano-Ronaldo-Stats",
     "Lionel Messi": "https://fbref.com/en/players/.../Lionel-Messi-Stats"
   }
   ```

2. **`unmatched_players.txt`** - Players not found in FBref index
   ```
   John Doe
   Unknown Player
   ```

3. **`player_url_summary.txt`** - Statistics report
   ```
   Total unique players in CSV: 2529
   Successfully matched: 2341 (92.6%)
   Not found: 188 (7.4%)
   ```

4. **`player_index_checkpoint.json`** - Resume file (auto-saved every 50 pages)

---

## Step 2: Scrape Player Statistics

Once you have `player_urls.json`, scrape detailed stats for all players.

### Run the Scraper

```bash
python3 scrape_multiple_players.py
```

### What It Does

1. Loads player URLs from `player_urls.json`
2. For each player:
   - Fetches their stats page
   - Extracts standard statistics table
   - Extracts defensive actions table
   - Saves to CSV files
3. Creates organized output folder with all data

### Expected Runtime

- **Depends on**: Number of matched players × delay
- **Example**: 2,341 players × 5 seconds = ~3.2 hours
- **Checkpointing**: Automatically saves progress

### Options

Edit the script or use it as a library:

```python
from scrape_multiple_players import scrape_multiple_players
import json

# Load URLs
with open('player_urls.json', 'r') as f:
    player_urls = json.load(f)

# Scrape first 10 players (for testing)
test_urls = dict(list(player_urls.items())[:10])
results = scrape_multiple_players(test_urls, delay=5)
```

### Output

For each player, creates CSV files in `outputs/` folder:

```
outputs/
├── Cristiano_Ronaldo_standard_stats.csv
├── Cristiano_Ronaldo_defensive_actions.csv
├── Lionel_Messi_standard_stats.csv
├── Lionel_Messi_defensive_actions.csv
└── ...
```

---

## File Structure

```
fbref_scrapper/
├── get_player_urls_from_csv.py    # Step 1: Find player URLs
├── scrape_multiple_players.py     # Step 2: Scrape stats
├── fbref_scraper.py                # Core scraper class
├── transfers_1.csv                 # Your input data
├── requirements.txt                # Python dependencies
│
├── player_urls.json                # Generated: Player URL mappings
├── unmatched_players.txt           # Generated: Players not found
├── player_url_summary.txt          # Generated: Statistics report
│
└── outputs/                        # Generated: Player stat CSVs
    ├── Player1_standard_stats.csv
    └── Player1_defensive_actions.csv
```

---

## Common Issues & Solutions

### Rate Limiting (429 or 403 Errors)

**Problem**: FBref blocks your IP after too many requests

**Solutions**:
1. **Increase delay**: `python3 get_player_urls_from_csv.py --delay 15`
2. **Wait 30-60 minutes** for rate limit to reset
3. **Use different network**: Switch WiFi, use mobile hotspot, or run on different machine
4. **Resume later**: Script auto-saves checkpoints, just run again

### Script Interrupted

**Solution**: Just run the same command again - it will resume from the checkpoint!

```bash
# Automatically resumes from last checkpoint
python3 get_player_urls_from_csv.py
```

### Low Match Rate

If many players are unmatched:

1. **Check player names** in CSV - are they spelled correctly?
2. **Check unmatched_players.txt** - look for patterns (nicknames, abbreviations, etc.)
3. **Manual lookup**: Search FBref manually for unmatched players

### Cloudflare Blocking

**Problem**: Cloudflare blocking despite using cloudscraper

**Solution**: This is rare, but if it happens:
1. Update cloudscraper: `pip install --upgrade cloudscraper`
2. Clear browser cookies/cache
3. Try from different network

---

## Tips for Running on School Lab Machine

1. **Clone repo to lab machine**:
   ```bash
   git clone <your-repo-url>
   cd fbref_scrapper
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run in background** (if SSH/remote):
   ```bash
   nohup python3 get_player_urls_from_csv.py > output.log 2>&1 &
   ```

4. **Monitor progress**:
   ```bash
   tail -f output.log
   ```

5. **Download results** when done:
   ```bash
   # From your local machine
   scp user@lab-machine:~/fbref_scrapper/player_urls.json .
   scp -r user@lab-machine:~/fbref_scrapper/outputs .
   ```

---

## Advanced Usage

### Scrape Specific Players Only

```python
from fbref_scraper import FBrefScraper

scraper = FBrefScraper(delay=5)

# Scrape one player
url = "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats"
results = scraper.scrape_player_stats(url)
scraper.save_results(results)
```

### Filter Players Before Scraping

```python
import json

# Load URLs
with open('player_urls.json', 'r') as f:
    all_urls = json.load(f)

# Filter by name pattern
premier_league_players = {
    name: url for name, url in all_urls.items()
    if 'specific_criteria' in name  # Customize filter
}

# Scrape filtered list
from scrape_multiple_players import scrape_multiple_players
scrape_multiple_players(premier_league_players, delay=5)
```

### Batch Processing

Split player list into batches:

```python
import json

with open('player_urls.json', 'r') as f:
    all_urls = json.load(f)

# Split into 10 batches
players_list = list(all_urls.items())
batch_size = len(players_list) // 10

for i in range(10):
    batch = dict(players_list[i*batch_size:(i+1)*batch_size])
    batch_file = f'batch_{i+1}_urls.json'

    with open(batch_file, 'w') as f:
        json.dump(batch, f, indent=2)

    print(f"Created {batch_file} with {len(batch)} players")
```

---

## Responsible Scraping

This tool is designed for **educational purposes** and follows web scraping best practices:

- ✅ Respects `robots.txt`
- ✅ Uses reasonable delays between requests (default: 5-8 seconds)
- ✅ Includes user-agent headers
- ✅ Implements checkpointing to avoid re-scraping
- ✅ Single-threaded (no aggressive parallel requests)

**Please:**
- Don't decrease delays below 3 seconds
- Don't run multiple instances simultaneously
- Don't scrape more data than you need
- Credit FBref.com when using the data

---

## Need Help?

1. **Check the logs** - Most errors are self-explanatory
2. **Review unmatched_players.txt** - See which players weren't found
3. **Increase delays** - If getting rate limited
4. **Wait and retry** - Rate limits are temporary

## Summary

```bash
# Complete workflow
pip install -r requirements.txt                    # Install
python3 get_player_urls_from_csv.py               # Find URLs (~25 min)
python3 scrape_multiple_players.py                 # Scrape stats (~3 hours)
```

Your data will be in:
- `player_urls.json` - URL mappings
- `outputs/*.csv` - Individual player statistics

Happy scraping! 🚀
