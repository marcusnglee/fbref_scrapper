# FBref Player Stats Scraper

A Python tool to automatically discover and scrape player statistics from FBref.com.

## Features

✅ **Smart URL Discovery** - Extracts unique players from CSV and finds their FBref URLs automatically
✅ **Efficient Scraping** - Only scrapes needed pages (saves 70% of time)
✅ **Cloudflare Bypass** - Uses cloudscraper to handle anti-bot protection
✅ **Auto-Checkpointing** - Resume interrupted scrapes
✅ **Rate Limit Friendly** - Respectful delays and error handling

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Get player URLs from your CSV
python3 get_player_urls_from_csv.py

# Step 2: Scrape player statistics
python3 scrape_multiple_players.py
```

## 📖 Full Documentation

**See [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) for detailed instructions, troubleshooting, and advanced usage.**

## Requirements

- Python 3.7+
- pandas
- cloudscraper
- beautifulsoup4
- requests

## Key Files

- **`get_player_urls_from_csv.py`** - Find FBref URLs for players in CSV
- **`scrape_multiple_players.py`** - Scrape stats for multiple players
- **`fbref_scraper.py`** - Core scraper class
- **`COMPLETE_GUIDE.md`** - Complete documentation

## Output

- `player_urls.json` - Player name → FBref URL mappings
- `outputs/*.csv` - Individual player statistics tables

## License

Educational use only. Please respect FBref.com's terms of service.
