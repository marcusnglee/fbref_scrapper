# 📦 FBref Web Scraping Project - Complete Package

## 🎯 What's Included

This package contains everything you need to scrape and analyze football statistics from FBref.com for your student project.

## 📁 Files in This Package

### 📘 Documentation
- **README.md** - Complete project overview and API reference
- **TUTORIAL.md** - Step-by-step guide for beginners  
- **PROJECT_SUMMARY.md** - This file (quick start guide)
- **requirements.txt** - Python dependencies

### 🐍 Python Scripts
- **fbref_scraper.py** - Main web scraper (live data from URLs)
- **fbref_parser.py** - HTML parser (works with saved files)
- **demo_extraction.py** - Working demo with sample data
- **run_demo.py** - Quick start script

### 📊 Sample Output Files (Kylian Mbappé)
- **Kylian_Mbappe_standard_stats.csv** - Goals, assists, minutes
- **Kylian_Mbappe_defensive_actions.csv** - Tackles, interceptions
- **Kylian_Mbappe_shooting.csv** - Shot metrics, xG
- **Kylian_Mbappe_passing.csv** - Pass completion, progressive passes
- **Kylian_Mbappe_info.json** - Player metadata
- **Kylian_Mbappe_all_stats.xlsx** - All tables in Excel

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test with Demo
```bash
python run_demo.py
```

### Step 3: Scrape Your Own Data

**Method A: From saved HTML (Recommended)**
```python
from fbref_parser import parse_from_file

# Save a player page from FBref as HTML
# Then parse it:
results = parse_from_file('your_player.html')
```

**Method B: Direct scraping**
```python
from fbref_scraper import FBrefScraper

scraper = FBrefScraper(delay=3)
results = scraper.scrape_player_stats('https://fbref.com/en/players/...')
scraper.save_results(results)
```

---

## 📊 What Data Can You Extract?

### Available Tables

✅ **Standard Stats**: Goals, assists, minutes, cards, xG  
✅ **Shooting**: Shot accuracy, conversion rate, xG breakdown  
✅ **Passing**: Completion %, progressive passes, key passes  
✅ **Pass Types**: Short/medium/long passes, crosses  
✅ **Goal & Shot Creation**: Actions leading to shots/goals  
✅ **Defensive Actions**: Tackles, interceptions, blocks  
✅ **Possession**: Touches, dribbles, carries  
✅ **Playing Time**: Match-by-match playing time  
✅ **Miscellaneous**: Fouls, offsides, aerials won  

---

## 💡 Project Ideas

### 1. Player Comparison Dashboard
Compare top strikers across multiple metrics

### 2. xG Analysis
Study which players outperform their expected goals

### 3. Defensive Forwards
Analyze attacking players' defensive contributions

### 4. Career Trajectory
Track a player's development season-by-season

### 5. League Comparison
Compare performance across different leagues

---

## 🎓 Perfect for Student Projects In:

- **Sports Analytics** courses
- **Data Science** projects
- **Web Scraping** assignments
- **Statistics** coursework
- **Python Programming** practice

---

## ⚖️ Important Notes

### ✅ Allowed Use
- Personal academic projects
- Research and learning
- Small-scale analysis (<100 players)

### ❌ Not Allowed
- Commercial use
- Large-scale automated scraping
- Redistributing data publicly
- Overwhelming FBref servers

### 🤝 Best Practices
1. Wait 3-5 seconds between requests
2. Scrape during off-peak hours
3. Save HTML locally to avoid re-scraping
4. Always cite FBref as your data source
5. Respect their robots.txt file

---

## 🔧 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum
- **Storage**: 100MB for dependencies + your data
- **Internet**: Only needed for initial scraping (not for parsing saved files)

---

## 📖 Learning Path

1. **Beginner**: Start with TUTORIAL.md
2. **Intermediate**: Read README.md for full documentation
3. **Advanced**: Modify fbref_scraper.py for custom needs

---

## 🎯 Sample Workflow

```
1. Choose players to analyze
2. Visit FBref and save pages as HTML
3. Run parser on saved files
4. Load CSV files in pandas
5. Calculate custom metrics
6. Create visualizations
7. Write your analysis report
```

---

## 📊 Sample Data Dictionary

### Standard Stats Columns
- `Gls` - Goals scored
- `Ast` - Assists
- `G+A` - Goals + Assists
- `90s` - 90-minute periods played
- `xG` - Expected Goals
- `npxG` - Non-Penalty Expected Goals
- `PrgC` - Progressive Carries
- `PrgP` - Progressive Passes

### Defensive Actions Columns
- `Tkl` - Tackles made
- `TklW` - Tackles won
- `Int` - Interceptions
- `Blocks` - Blocked shots/passes
- `Clr` - Clearances

---

## 🔗 Useful Links

- **FBref**: https://fbref.com
- **FBref Glossary**: https://fbref.com/en/about/glossary.html
- **Pandas Docs**: https://pandas.pydata.org
- **Python Web Scraping**: https://realpython.com/beautiful-soup-web-scraper-python/

---

## 💻 Example Analysis Code

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('Kylian_Mbappe_standard_stats.csv')

# Calculate per-90 metrics
df['G_per_90'] = df['Gls'] / df['90s']

# Visualize
plt.figure(figsize=(10, 6))
plt.bar(df['Season'], df['G_per_90'])
plt.title('Goals per 90 Minutes by Season')
plt.xlabel('Season')
plt.ylabel('Goals per 90')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('goals_per_90.png')
plt.show()
```

---

## ✅ Pre-Flight Checklist

Before starting your project:

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Demo script runs successfully
- [ ] Understand robots.txt and rate limits
- [ ] Have list of players to analyze
- [ ] Know which metrics you want to study
- [ ] Have citation format ready
- [ ] Understand basic pandas operations

---

## 🎓 Citation Template

```
Data Source: FBref.com, powered by Stats Perform Opta data.
Player statistics extracted using responsible web scraping practices
with appropriate rate limiting and respect for terms of service.

Example:
"Kylian Mbappé Stats," FBref.com, accessed December 6, 2025,
https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats
```

---

## 🆘 Getting Help

**Code Issues**: Check TUTORIAL.md troubleshooting section  
**Data Questions**: See FBref glossary  
**Python Help**: pandas documentation  
**Project Ideas**: See project examples in TUTORIAL.md

---

## 🎉 You're All Set!

You now have everything you need to:
- ✅ Scrape football statistics responsibly
- ✅ Parse and clean the data
- ✅ Analyze player performance
- ✅ Create compelling visualizations
- ✅ Complete your student project

**Next Step**: Open TUTORIAL.md and follow along!

Good luck with your project! ⚽📊🎓

---

*Last Updated: December 6, 2025*  
*Package Version: 1.0*  
*For Educational Use Only*
