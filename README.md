# FBref Web Scraping Guide for Student Projects

## 📋 Overview

This project provides Python scripts to extract football player statistics from FBref.com for academic research and analysis. The scripts are designed to respect FBref's robots.txt and implement responsible scraping practices.

## 🎯 What This Project Does

Extracts player statistics tables from FBref including:
- **Standard Stats**: Goals, assists, minutes played, etc.
- **Defensive Actions**: Tackles, interceptions, blocks
- **Shooting**: Shot accuracy, xG metrics
- **Passing**: Completion rates, progressive passes
- And more...

## 📁 Project Files

1. **`fbref_scraper.py`** - Full web scraper (requires internet)
2. **`fbref_parser.py`** - Parser for local HTML files
3. **`demo_extraction.py`** - Working demo with sample data
4. **`extract_mbappe_stats.py`** - Example extraction script

## 🚀 Quick Start

### Method 1: Using Saved HTML Files (Recommended for Students)

This is the best method as it:
- Respects rate limits (save once, analyze forever)
- Works offline
- No network issues

```python
from fbref_parser import parse_from_file

# Step 1: Save any FBref player page as HTML (Ctrl+S in browser)
# Step 2: Parse it
results = parse_from_file('mbappe_stats.html')
```

### Method 2: Direct Web Scraping (When Network Allows)

```python
from fbref_scraper import FBrefScraper

scraper = FBrefScraper(delay=3)  # 3 second delay between requests
results = scraper.scrape_player_stats(
    'https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats'
)
scraper.save_results(results)
```

## 📊 Output Files

The scripts create:

1. **Individual CSV files** for each stats table:
   - `PlayerName_standard_stats.csv`
   - `PlayerName_defensive_actions.csv`
   - `PlayerName_shooting.csv`
   - etc.

2. **JSON file** with player metadata:
   - `PlayerName_info.json`

3. **Excel workbook** with all tables:
   - `PlayerName_all_stats.xlsx` (multiple sheets)

## 💻 Installation

```bash
# Install required packages
pip install pandas beautifulsoup4 requests openpyxl lxml

# Or use requirements.txt
pip install -r requirements.txt
```

## 🔧 Usage Examples

### Example 1: Single Player

```python
from fbref_parser import FBrefParser

# Read HTML file
with open('mbappe.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Parse it
parser = FBrefParser()
results = parser.parse_html(html)

# Access specific tables
standard_stats = results['standard_stats']
defensive_stats = results['defensive_actions']

# Save everything
parser.save_results(results)
```

### Example 2: Multiple Players

```python
from fbref_parser import parse_from_file
import os

# List of saved HTML files
players = [
    'mbappe.html',
    'haaland.html',
    'salah.html'
]

all_results = {}

for player_file in players:
    print(f"Processing {player_file}...")
    results = parse_from_file(player_file)
    
    # Store for comparison
    player_name = results['player_info']['player_name']
    all_results[player_name] = results
    
print(f"Processed {len(all_results)} players")
```

### Example 3: Comparing Stats

```python
import pandas as pd

# Combine standard stats from multiple players
all_standard_stats = []

for player_name, results in all_results.items():
    df = results['standard_stats']
    df['player'] = player_name
    all_standard_stats.append(df)

# Create comparison dataframe
comparison = pd.concat(all_standard_stats, ignore_index=True)

# Analyze
top_scorers = comparison.nlargest(10, 'Gls')
print(top_scorers[['player', 'Season', 'Gls', 'Ast']])
```

## 📖 Understanding the Data

### Standard Stats Table Columns

- **MP**: Matches Played
- **Starts**: Games Started
- **Min**: Minutes Played
- **90s**: Minutes / 90 (equivalent full games)
- **Gls**: Goals
- **Ast**: Assists
- **G+A**: Goals + Assists
- **G-PK**: Non-Penalty Goals
- **PK**: Penalty Kicks Made
- **PKatt**: Penalty Kicks Attempted
- **xG**: Expected Goals
- **npxG**: Non-Penalty Expected Goals
- **xAG**: Expected Assisted Goals
- **PrgC**: Progressive Carries
- **PrgP**: Progressive Passes
- **PrgR**: Progressive Passes Received

### Defensive Actions Table Columns

- **Tkl**: Tackles
- **TklW**: Tackles Won
- **Def 3rd**: Tackles in Defensive Third
- **Mid 3rd**: Tackles in Middle Third
- **Att 3rd**: Tackles in Attacking Third
- **Int**: Interceptions
- **Blocks**: Blocks
- **Clr**: Clearances
- **Err**: Errors

## ⚖️ Legal & Ethical Considerations

### ✅ Appropriate Use

- Personal academic projects
- Research and analysis
- Learning web scraping techniques
- Small-scale data collection (<100 players)

### ❌ Not Allowed

- Commercial use without permission
- Redistributing scraped data
- Overwhelming FBref servers
- Automated large-scale scraping

### 🤝 Best Practices

1. **Respect Rate Limits**: Wait 3-5 seconds between requests
2. **Identify Yourself**: Use descriptive User-Agent
3. **Cache Results**: Save HTML locally to avoid re-scraping
4. **Off-Peak Hours**: Scrape during late night/early morning
5. **Check robots.txt**: Always review before scraping

## 🎓 Student Project Ideas

### 1. Player Performance Analysis
Compare attacking metrics across top forwards:
```python
# Analyze goals per 90 vs xG
comparison['goals_per_90'] = comparison['Gls'] / comparison['90s']
comparison['xg_per_90'] = comparison['xG'] / comparison['90s']
comparison['overperformance'] = comparison['goals_per_90'] - comparison['xg_per_90']
```

### 2. Defensive Contribution Study
Analyze defensive actions by position:
```python
# Forwards who defend
defensive = results['defensive_actions']
defensive['tackles_per_90'] = defensive['Tkl'] / standard_stats['90s']
```

### 3. Season-Over-Season Trends
Track player development:
```python
# Get all seasons for one player
seasons = standard_stats.sort_values('Season')
seasons.plot(x='Season', y=['Gls', 'Ast'])
```

### 4. xG Analysis
Compare expected vs actual goals:
```python
shooting = results['shooting']
shooting['xG_diff'] = shooting['Gls'] - shooting['xG']
# Players outperforming xG
```

## 🐛 Troubleshooting

### Network Errors
**Problem**: Can't connect to FBref
**Solution**: Use Method 1 (save HTML first)

### Missing Tables
**Problem**: Some stats tables not extracted
**Solution**: Check if table exists on the page (not all players have all tables)

### Encoding Errors
**Problem**: Special characters not displaying
**Solution**: Use `encoding='utf-8'` when reading files

### Empty DataFrames
**Problem**: Tables extracted but empty
**Solution**: Check HTML structure - FBref may have updated their layout

## 📚 Resources

- **FBref**: https://fbref.com
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **BeautifulSoup Guide**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Web Scraping Ethics**: https://en.wikipedia.org/wiki/Web_scraping#Legal_issues

## 📝 Sample Analysis Script

```python
"""
Sample analysis: Top scorers in current season
"""
import pandas as pd
from fbref_parser import parse_from_file

# Load data
results = parse_from_file('mbappe.html')
stats = results['standard_stats']

# Filter current season
current = stats[stats['Season'] == '2025-2026']

# Calculate per-90 metrics
current['Goals_per_90'] = current['Gls'] / current['90s']
current['Assists_per_90'] = current['Ast'] / current['90s']
current['G+A_per_90'] = current['G+A'] / current['90s']

# Display
print(current[['Squad', 'Gls', 'Ast', 'Goals_per_90', 'G+A_per_90']])
```

## 🎬 Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Install required packages (`pip install -r requirements.txt`)
- [ ] Visit FBref and save a player page as HTML
- [ ] Run `demo_extraction.py` to test
- [ ] Parse your saved HTML file
- [ ] Explore the output CSV/Excel files
- [ ] Start your analysis!

## 📧 Questions?

This is a student project template. Adapt it for your specific needs!

Remember to:
- Cite FBref as your data source
- Respect their terms of service
- Use data responsibly
- Give proper attribution in your project

---

**Last Updated**: December 2025
**License**: Educational Use Only
**Data Source**: FBref.com (Stats Perform Opta data)
