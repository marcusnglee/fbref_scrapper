# How to Use the FBref Scraper

## Summary

The scraper is now working successfully! It uses `cloudscraper` to bypass Cloudflare protection.

## What Was Fixed

1. **Cloudflare Protection**: Installed and integrated `cloudscraper` package
2. **Output Directory**: Changed from `/mnt/user-data/outputs` to `./outputs`
3. **Rate Limiting**: Added conservative delays between requests

## Quick Start

### 1. Single Player

```python
from fbref_scraper import FBrefScraper

scraper = FBrefScraper(delay=5)
results = scraper.scrape_player_stats("https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats")
scraper.save_results(results)
```

### 2. Multiple Players

```bash
python3 scrape_multiple_players.py
```

Edit the `players` dictionary in `scrape_multiple_players.py` to add your player URLs.

## Important Best Practices

### Rate Limiting

- **Minimum delay**: 5 seconds between requests
- **Recommended delay**: 8-10 seconds for large batches
- FBref may return 500 errors if you scrape too quickly
- If you get 500 errors, wait 30-60 seconds and increase the delay

### Finding Player URLs

1. Go to fbref.com
2. Search for a player
3. Copy the URL from their stats page
4. Format: `https://fbref.com/en/players/{player_id}/{player_name}-Stats`

### Example Player URLs

```python
players = {
    "Kylian Mbappé": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats",
    "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
    "Mohamed Salah": "https://fbref.com/en/players/e342ad68/Mohamed-Salah-Stats",
    "Kevin De Bruyne": "https://fbref.com/en/players/e46012d4/Kevin-De-Bruyne-Stats",
    "Harry Kane": "https://fbref.com/en/players/21a66f6a/Harry-Kane-Stats",
}
```

## Output Files

For each player, you'll get:

1. **CSV files** (9 tables per player):
   - `{PlayerName}_standard_stats.csv`
   - `{PlayerName}_defensive_actions.csv`
   - `{PlayerName}_shooting.csv`
   - `{PlayerName}_passing.csv`
   - `{PlayerName}_pass_types.csv`
   - `{PlayerName}_goal_shot_creation.csv`
   - `{PlayerName}_possession.csv`
   - `{PlayerName}_playing_time.csv`
   - `{PlayerName}_misc.csv`

2. **Excel file**: `{PlayerName}_all_stats.xlsx` (all tables in one file)

3. **JSON file**: `{PlayerName}_info.json` (metadata)

## Data Included

### Standard Stats
Goals, assists, minutes played, xG, npxG, progressive carries/passes, etc.

### Defensive Actions
Tackles, interceptions, blocks, clearances, errors

### Other Tables
Shooting, passing, pass types, goal/shot creation, possession, playing time, miscellaneous stats

## Tips for Large-Scale Scraping

### 1. Batch Processing

Scrape in batches of 10-20 players at a time with breaks:

```python
# Batch 1: Top 20 strikers
# Wait 5 minutes
# Batch 2: Top 20 midfielders
# etc.
```

### 2. Save Progress

The scraper saves each player immediately after scraping, so if it fails partway through, you won't lose previous data.

### 3. Resume After Errors

If you get rate limited:
1. Wait 5-10 minutes
2. Remove successfully scraped players from your list
3. Increase the delay parameter
4. Resume with remaining players

### 4. Run During Off-Peak Hours

FBref has less traffic late at night (US time), making scraping more reliable.

## Example: Scrape Top 50 Players

```python
from scrape_multiple_players import scrape_multiple_players

# Split into batches
batch_1 = {
    "Player 1": "url1",
    "Player 2": "url2",
    # ... up to 10 players
}

batch_2 = {
    "Player 11": "url11",
    # ... next 10 players
}

# Scrape batch 1
print("Scraping Batch 1...")
scrape_multiple_players(batch_1, delay=8)

# Wait between batches
import time
print("Waiting 5 minutes before next batch...")
time.sleep(300)

# Scrape batch 2
print("Scraping Batch 2...")
scrape_multiple_players(batch_2, delay=8)
```

## Troubleshooting

### 403 Forbidden
- Should not happen anymore with cloudscraper
- If it does, try increasing delay

### 500 Server Error
- You're being rate limited
- Wait 5-10 minutes
- Increase delay to 10+ seconds

### Connection Timeout
- Network issue or FBref is down
- Try again in a few minutes

### Missing Tables
- Not all players have all tables
- This is normal (e.g., goalkeepers don't have shooting stats)

## Ethical Guidelines

1. **Respect rate limits**: Use 5+ second delays
2. **Don't overload servers**: Batch your requests
3. **Academic use only**: This is for student projects
4. **Cite FBref**: Always credit FBref.com as your data source
5. **No redistribution**: Don't share scraped datasets publicly

## Current Status

✅ Scraper is working
✅ Cloudflare bypass implemented
✅ Multiple player support ready
✅ Data successfully extracted for:
  - Kylian Mbappé
  - Erling Haaland

Ready to scale up to more players!
