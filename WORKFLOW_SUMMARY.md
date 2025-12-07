# Complete Workflow Summary

## 🎯 Goal
Analyze player statistics from the season BEFORE they were transferred, combined across all clubs they played for that season.

## 📊 Data Flow

```
transfers_1.csv (2,529 transfers)
         ↓
    (Extract unique players)
         ↓
transfers_player_urls.json (2,191 matched players)
         ↓
    (Split into 4 batches)
         ↓
batch_1_player_urls.json (548 players)
batch_2_player_urls.json (548 players)
batch_3_player_urls.json (548 players)
batch_4_player_urls.json (547 players)
         ↓
    (Scrape each batch)
         ↓
outputs/*.csv (individual player stats)
         ↓
    (Merge with transfers)
         ↓
merged_transfer_stats.csv (final dataset)
```

## 🔧 Step-by-Step Execution

### ✅ COMPLETED

1. **Extract Player URLs**
   ```bash
   python3 get_player_urls_from_csv.py
   ```
   - Output: `player_urls.json` (all FBref players)

2. **Filter to Transfer Players Only**
   ```bash
   python3 filter_player_urls.py
   ```
   - Output: `transfers_player_urls.json` (2,191 matched)
   - Output: `transfers_unmatched_players.txt` (338 not found)

3. **Create 4 Batches**
   ```bash
   python3 create_batches.py
   ```
   - Output: `batch_1_player_urls.json` through `batch_4_player_urls.json`

### 🚀 TODO: Scraping (Run on Lab Machines)

**Each batch takes ~2.3 hours with 15-second delay**

Run these in parallel on different lab machines:

```bash
# Machine 1 - Batch 1 (548 players)
python3 scrape_batch.py batch_1_player_urls.json

# Machine 2 - Batch 2 (548 players)
python3 scrape_batch.py batch_2_player_urls.json

# Machine 3 - Batch 3 (548 players)
python3 scrape_batch.py batch_3_player_urls.json

# Machine 4 - Batch 4 (547 players)
python3 scrape_batch.py batch_4_player_urls.json
```

**Output:** Individual CSV files in `outputs/` folder:
- `{Player}_standard_stats.csv`
- `{Player}_defensive_actions.csv`

### 🔄 Final Step: Merge Data

After all batches complete:

```bash
python3 merge_transfer_stats.py
```

**What this does:**
1. Reads `transfers_1.csv`
2. For each transfer in season "XX/YY":
   - Converts to previous season (e.g., "10/11" → look for "2009-2010")
   - Finds player's stats CSV in `outputs/`
   - Extracts stats from that season
   - If player played for multiple clubs that season, combines stats
   - Merges with transfer data
3. Outputs: `merged_transfer_stats.csv`

**Output columns:**
- All original transfer data (Player, Fee, Season, Age, Position, etc.)
- `Stats_*` columns: Standard stats from previous season (Goals, Assists, Minutes, etc.)
- `Def_*` columns: Defensive stats from previous season (Tackles, Interceptions, etc.)
- `Stats_Season`: Which season the stats are from

## 📈 Example Result

For Fernando Torres transferred in '10/11' season:

| Player | Season | Fee | Left Club | Stats_Season | Stats_Gls | Stats_Ast | Stats_Min |
|--------|--------|-----|-----------|--------------|-----------|-----------|-----------|
| Fernando Torres | 10/11 | €58.50m | Liverpool | 2009-2010 | 18 | 9 | 2730 |

This shows his 2009-2010 season stats (the full season BEFORE his Jan 2011 transfer).

## 🎓 Analysis Ideas

Once you have `merged_transfer_stats.csv`, you can analyze:

1. **Performance vs Transfer Fee**
   ```python
   import pandas as pd
   df = pd.read_csv('merged_transfer_stats.csv')

   # Goals vs Fee
   df.plot.scatter(x='Stats_Gls', y='Fee (€)')
   ```

2. **Position-specific Metrics**
   ```python
   # Strikers: Goals per 90
   strikers = df[df['Position'].str.contains('Forward')]
   strikers['Gls_per_90'] = strikers['Stats_Gls'] / strikers['Stats_90s']
   ```

3. **League Differences**
   ```python
   # Compare players coming FROM different leagues
   df.groupby('Left League')['Stats_Gls'].mean()
   ```

4. **Age Analysis**
   ```python
   # Peak transfer age
   df.groupby('Age')['Fee (€)'].mean().plot()
   ```

## ⚙️ Technical Details

### Season Matching Logic

Transfer season format: `"10/11"` (when transfer happened)
FBref season format: `"2010-2011"`

**Conversion:**
- Transfer in "10/11" → Previous season is "09/10" → FBref "2009-2010"
- This gets the last FULL season before transfer

### Stat Aggregation

If a player played for multiple clubs in the previous season:
- **Numeric columns**: Summed (Goals, Assists, Minutes, etc.)
- **Non-numeric columns**: First value taken
- **Squad column**: Set to "Combined"

Example: Player with loan spell + parent club in same season gets combined stats.

## 📁 File Structure After Completion

```
fbref_scrapper/
├── transfers_1.csv                    # Original transfer data
├── transfers_player_urls.json         # Matched player URLs
├── batch_1_player_urls.json          # Batch files
├── batch_2_player_urls.json
├── batch_3_player_urls.json
├── batch_4_player_urls.json
│
├── outputs/                           # Scraped stats (2,191+ files)
│   ├── Fernando_Torres_standard_stats.csv
│   ├── Fernando_Torres_defensive_actions.csv
│   └── ...
│
└── merged_transfer_stats.csv         # FINAL OUTPUT
```

## 🚨 Important Notes

1. **Scraping Time**
   - 4 batches × ~2.3 hours = ~9.2 hours total
   - Can be reduced to ~2.3 hours if run in parallel on 4 machines

2. **Missing Data**
   - Some players won't have stats for previous season (rookies, youth players)
   - These will be logged in `merge_not_found.csv`

3. **Data Quality**
   - Combined stats are summed (assumes additive metrics like goals, minutes)
   - Rates (per 90 stats) should be recalculated after merging

4. **Resume Capability**
   - Each batch saves progress as it scrapes
   - If interrupted, just restart the batch script

## 📝 Next Steps

1. ✅ Setup complete
2. 🔄 Run 4 batch scrapes (parallel on lab machines)
3. 📥 Collect all `outputs/` files
4. 🔗 Run merge script
5. 📊 Analyze!

Good luck with your analysis! 🚀
