# Quick Start Guide - FBref Scraper

## What's Changed

✅ **Scraper now only extracts:**
- Standard Stats CSV
- Defensive Actions CSV

✅ **Can get player URLs automatically** from team/league pages

## Basic Workflow

### Step 1: Get Player URLs

#### Option A: From a Team's Squad Page

```python
from get_player_urls import get_player_urls_from_squad, save_urls_to_file

# Real Madrid example
team_url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
players = get_player_urls_from_squad(team_url, delay=3)

# Save to JSON file
save_urls_to_file(players, 'my_players.json')
```

#### Option B: From a League Stats Page

```python
from get_player_urls import get_player_urls_from_league_stats, save_urls_to_file

# Premier League top players
league_url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
players = get_player_urls_from_league_stats(league_url, delay=3)

save_urls_to_file(players, 'premier_league_players.json')
```

#### Option C: Manual List

```python
players = {
    "Kylian Mbappé": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats",
    "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
    "Mohamed Salah": "https://fbref.com/en/players/e342ad68/Mohamed-Salah-Stats",
}

import json
with open('my_players.json', 'w') as f:
    json.dump(players, f, indent=2)
```

### Step 2: Scrape the Players

```python
from scrape_multiple_players import scrape_multiple_players
import json

# Load player URLs
with open('my_players.json', 'r') as f:
    players = json.load(f)

# Scrape all players
results = scrape_multiple_players(players, delay=8)
```

### Step 3: Check Output

All CSV files will be in the `outputs/` folder:
```
outputs/
├── PlayerName_standard_stats.csv
├── PlayerName_defensive_actions.csv
├── AnotherPlayer_standard_stats.csv
├── AnotherPlayer_defensive_actions.csv
...
```

## Complete Example

```python
# complete_example.py

# 1. Get URLs from Real Madrid squad
from get_player_urls import get_player_urls_from_squad
from scrape_multiple_players import scrape_multiple_players
import time

print("Step 1: Getting player URLs...")
real_madrid_url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
players = get_player_urls_from_squad(real_madrid_url, delay=3)

print(f"Found {len(players)} players")

# 2. Scrape first 5 players (for testing)
test_players = dict(list(players.items())[:5])

print(f"\nStep 2: Scraping {len(test_players)} players...")
results = scrape_multiple_players(test_players, delay=8)

print(f"\nDone! Check the 'outputs/' folder for CSV files")
```

## Data Format

### Standard Stats CSV Columns
- Season, Age, Squad, Competition
- MP (Matches Played), Starts, Min (Minutes)
- Performance: Gls, Ast, G+A, xG, npxG, xAG
- Per 90 Minutes: Goals, Assists, etc.
- Progression: PrgC, PrgP, PrgR

### Defensive Actions CSV Columns
- Season, Age, Squad, Competition
- Tackles: Tkl, TklW, Def 3rd, Mid 3rd, Att 3rd
- Challenges: Tkl, Att, Tkl%
- Blocks: Blocks, Sh, Pass
- Int (Interceptions), Clr (Clearances), Err (Errors)

## Common Team URLs

See `TEAM_URLS.md` for a comprehensive list of team URLs.

Quick examples:
```python
teams = {
    "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats",
    "Barcelona": "https://fbref.com/en/squads/206d90db/Barcelona-Stats",
    "Man City": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "Bayern": "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats",
}
```

## Tips

### For Many Players (100+)
1. Get all URLs first and save to JSON
2. Scrape in batches of 20-30
3. Use 8-10 second delays
4. Take 5-10 minute breaks between batches

```python
# Batch processing example
all_players = {...}  # Your full list

# Split into batches of 20
batch_size = 20
player_items = list(all_players.items())

for i in range(0, len(player_items), batch_size):
    batch = dict(player_items[i:i+batch_size])
    print(f"Batch {i//batch_size + 1}: Scraping {len(batch)} players...")

    scrape_multiple_players(batch, delay=8)

    if i + batch_size < len(player_items):
        print("Waiting 5 minutes before next batch...")
        time.sleep(300)
```

### Rate Limiting
- **Minimum delay**: 5 seconds
- **Recommended**: 8-10 seconds
- **If you get 500 errors**: Wait 10 minutes, increase delay to 12+ seconds

### Resume After Interruption
Since each player is saved immediately, you can:
1. Check which players already have CSV files
2. Remove them from your list
3. Resume scraping the remaining players

```python
import os

# Check which players are done
done_players = []
for file in os.listdir('outputs'):
    if '_standard_stats.csv' in file:
        player_name = file.replace('_standard_stats.csv', '').replace('_', ' ')
        done_players.append(player_name)

print(f"Already scraped: {len(done_players)} players")
```

## Troubleshooting

**403 Forbidden**: Should not happen with cloudscraper
**500 Server Error**: Rate limited - wait and increase delay
**Empty CSV**: Player might not have that data available
**Missing players**: Some links might be invalid - check the JSON file

## Files in This Project

- `fbref_scraper.py` - Main scraper (updated for 2 tables only)
- `scrape_multiple_players.py` - Batch scraping utility
- `get_player_urls.py` - Extract URLs from team/league pages
- `TEAM_URLS.md` - Reference of common team URLs
- `QUICK_START.md` - This file
