# Updated FBref Scraper - Summary

## Changes Made

### 1. Scraper Modified ✅
- **Now only scrapes 2 tables** instead of 9:
  - Standard Stats
  - Defensive Actions
- **Output**: Only CSV files (no Excel, no JSON)
- **Faster**: ~3 seconds per player instead of ~10 seconds

### 2. URL Extraction Tool Added ✅
- **Automatic URL extraction** from:
  - Team/squad pages
  - League stats pages
- **Filters out** non-player links automatically
- **Saves to JSON** for easy reuse

### 3. Complete Workflow Created ✅
- Get URLs → Save to JSON → Scrape players
- Multiple example scripts provided
- Resume capability (scrape from saved JSON)

## Current Status

### Successfully Scraped Players
```
outputs/
├── Kylian_Mbappé_standard_stats.csv
├── Kylian_Mbappé_defensive_actions.csv
├── Erling_Haaland_standard_stats.csv
├── Erling_Haaland_defensive_actions.csv
├── Mohamed_Salah_standard_stats.csv
├── Mohamed_Salah_defensive_actions.csv
```

### Extracted Player URLs
```
real_madrid_players.json - 52 players
```

## Quick Usage

### Get Player URLs from a Team
```python
from get_player_urls import get_player_urls_from_squad, save_urls_to_file

# Example: Real Madrid
url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
players = get_player_urls_from_squad(url, delay=3)
save_urls_to_file(players, 'my_team.json')
```

### Scrape Players
```python
from scrape_multiple_players import scrape_multiple_players
import json

# Load URLs
with open('my_team.json', 'r') as f:
    players = json.load(f)

# Scrape
results = scrape_multiple_players(players, delay=8)
```

### Or Use the Interactive Example
```bash
python3 example_complete_workflow.py
```

## File Overview

### Core Files
| File | Purpose |
|------|---------|
| `fbref_scraper.py` | Main scraper class (updated for 2 tables only) |
| `scrape_multiple_players.py` | Batch scraping utility |
| `get_player_urls.py` | Extract URLs from team/league pages |

### Example Scripts
| File | Purpose |
|------|---------|
| `example_complete_workflow.py` | Interactive examples (recommended) |
| `scrape_team_workflow.py` | Complete workflow for one team |
| `test_scraper_conservative.py` | Simple test script |

### Documentation
| File | Purpose |
|------|---------|
| `QUICK_START.md` | **Start here** - Basic usage guide |
| `TEAM_URLS.md` | Common team URLs reference |
| `HOW_TO_USE.md` | Detailed usage instructions |
| `UPDATED_SUMMARY.md` | This file |

## What You Can Do Now

### 1. Scrape a Single Team
```bash
python3 -c "
from get_player_urls import get_player_urls_from_squad
from scrape_multiple_players import scrape_multiple_players

# Manchester City
url = 'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats'
players = get_player_urls_from_squad(url, delay=3)
scrape_multiple_players(players, delay=8)
"
```

### 2. Scrape Multiple Teams
```python
# get_multiple_teams.py
from get_player_urls import get_player_urls_from_squad, save_urls_to_file
import time

teams = {
    "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats",
    "Barcelona": "https://fbref.com/en/squads/206d90db/Barcelona-Stats",
    "Man City": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
}

all_players = {}
for name, url in teams.items():
    print(f"Getting {name}...")
    players = get_player_urls_from_squad(url, delay=3)
    all_players.update(players)
    time.sleep(5)

save_urls_to_file(all_players, 'all_players.json')
print(f"Total: {len(all_players)} players")

# Then scrape
from scrape_multiple_players import scrape_multiple_players
scrape_multiple_players(all_players, delay=8)
```

### 3. Scrape Top Players from a League
```python
from get_player_urls import get_player_urls_from_league_stats
from scrape_multiple_players import scrape_multiple_players

# Premier League
url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
players = get_player_urls_from_league_stats(url, delay=3)
scrape_multiple_players(players, delay=8)
```

## Output Format

### Standard Stats CSV
Each row = one season for the player

Columns include:
- Season, Age, Squad, Competition, League Rank
- Playing Time: MP, Starts, Min, 90s
- Performance: Gls, Ast, G+A, G-PK, PK, PKatt, Cards
- Expected: xG, npxG, xAG, npxG+xAG
- Progression: PrgC, PrgP, PrgR
- Per 90 Minutes: All stats normalized

### Defensive Actions CSV
Each row = one season for the player

Columns include:
- Season, Age, Squad, Competition, League Rank
- 90s (matches played)
- Tackles: Tkl, TklW, Def 3rd, Mid 3rd, Att 3rd
- Challenges: Tkl, Att, Tkl%, Lost
- Blocks: Blocks, Sh, Pass
- Int (Interceptions)
- Tkl+Int
- Clr (Clearances)
- Err (Errors)

## Best Practices for Large-Scale Scraping

### For 50-100 Players
1. Get all URLs first → save to JSON
2. Scrape in 2-3 batches of ~30 players
3. Use 8-10 second delays
4. Take 5-10 minute breaks between batches

### For 100-500 Players
1. Get URLs → save to JSON
2. Scrape in batches of 20-25
3. Use 10-12 second delays
4. Take 10-15 minute breaks between batches
5. Run during off-peak hours (late night US time)

### Example Batch Script
```python
import json
from scrape_multiple_players import scrape_multiple_players
import time

# Load all players
with open('all_players.json', 'r') as f:
    all_players = json.load(f)

# Batch processing
batch_size = 20
items = list(all_players.items())

for i in range(0, len(items), batch_size):
    batch = dict(items[i:i+batch_size])
    batch_num = i // batch_size + 1

    print(f"\nBatch {batch_num}: {len(batch)} players")
    scrape_multiple_players(batch, delay=10)

    # Break between batches (except last one)
    if i + batch_size < len(items):
        print("Waiting 10 minutes...")
        time.sleep(600)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 500 Server Error | Rate limited - wait 10 min, increase delay |
| 403 Forbidden | Shouldn't happen with cloudscraper |
| Empty CSV | Player may not have that data |
| Script stops | It auto-saves each player, just resume |

## Next Steps

1. **Read**: `QUICK_START.md` for basic usage
2. **Try**: `python3 example_complete_workflow.py`
3. **Reference**: `TEAM_URLS.md` for team URLs
4. **Scale up**: Use batch processing for many players

## Summary

✅ Scraper working and optimized (2 tables only)
✅ URL extraction tools ready
✅ Successfully tested on 3 players
✅ Complete workflow examples provided
✅ Ready to scale to hundreds of players

**You're ready to start scraping!** 🚀
