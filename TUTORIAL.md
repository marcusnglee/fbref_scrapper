# 🎓 Step-by-Step Tutorial: Web Scraping FBref for Your Student Project

## 🎯 What You'll Learn
- How to extract football statistics from FBref.com
- Responsible web scraping practices
- Data analysis with pandas
- Creating visualizations from scraped data

---

## 📦 Step 1: Setup Your Environment

### Install Python (if not already installed)
1. Download Python 3.8+ from https://python.org
2. Check installation: `python --version`

### Install Required Packages

```bash
# Navigate to your project folder
cd /path/to/your/project

# Install dependencies
pip install -r requirements.txt
```

**What gets installed:**
- `pandas` - Data manipulation
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `openpyxl` - Excel file support
- `lxml` - Fast HTML processing

---

## 🌐 Step 2: Collect Your Data

### Option A: Save HTML Pages (RECOMMENDED for students)

**Why this method?**
- ✅ No rate limiting issues
- ✅ Works offline
- ✅ Can review before scraping
- ✅ No network errors

**How to save:**

1. **Visit FBref.com**
   - Example: https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats

2. **Save the page**
   - Press `Ctrl + S` (Windows/Linux) or `Cmd + S` (Mac)
   - Choose "Webpage, Complete" or "HTML Only"
   - Save as `mbappe.html` in your project folder

3. **Repeat for other players you want to analyze**

### Option B: Direct Web Scraping (Advanced)

```python
from fbref_scraper import FBrefScraper

scraper = FBrefScraper(delay=3)  # Wait 3 seconds between requests
results = scraper.scrape_player_stats(
    'https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats'
)
scraper.save_results(results)
```

⚠️ **Important**: Always respect rate limits! Wait 3-5 seconds between requests.

---

## 🔍 Step 3: Extract the Data

### Quick Test - Run the Demo

```bash
python run_demo.py
```

This will show you how the extraction works with sample data.

### Extract from Your Saved HTML

```python
from fbref_parser import parse_from_file

# Parse the saved HTML file
results = parse_from_file('mbappe.html')

# Results is a dictionary containing:
# - player_info: Name, position, etc.
# - standard_stats: Goals, assists, minutes
# - defensive_actions: Tackles, interceptions
# - shooting: Shot accuracy, xG
# - passing: Pass completion, progressive passes
# - And more...
```

### What You Get

After running the script, you'll have:

```
your_project_folder/
├── Kylian_Mbappe_standard_stats.csv      ← Main statistics
├── Kylian_Mbappe_defensive_actions.csv   ← Defensive metrics
├── Kylian_Mbappe_shooting.csv            ← Shooting statistics
├── Kylian_Mbappe_passing.csv             ← Passing metrics
├── Kylian_Mbappe_info.json               ← Player metadata
└── Kylian_Mbappe_all_stats.xlsx          ← Everything in one file
```

---

## 📊 Step 4: Analyze Your Data

### Example 1: Load and Explore

```python
import pandas as pd

# Load the standard stats
df = pd.read_csv('Kylian_Mbappe_standard_stats.csv')

# View the data
print(df.head())
print(df.columns)
print(df.describe())

# Check most recent season
current_season = df[df['Season'] == '2025-2026']
print(f"Goals this season: {current_season['Gls'].values[0]}")
print(f"Assists this season: {current_season['Ast'].values[0]}")
```

### Example 2: Calculate Per-90 Metrics

```python
# Goals per 90 minutes
df['Goals_per_90'] = df['Gls'] / df['90s']
df['Assists_per_90'] = df['Ast'] / df['90s']
df['G+A_per_90'] = df['G+A'] / df['90s']

# Show results
print(df[['Season', 'Squad', 'Goals_per_90', 'Assists_per_90']].round(2))
```

### Example 3: Compare xG vs Actual Goals

```python
# Expected Goals analysis
df['xG_overperformance'] = df['Gls'] - df['xG']
df['npxG_overperformance'] = df['G-PK'] - df['npxG']

# Which seasons did he overperform?
print(df[['Season', 'Gls', 'xG', 'xG_overperformance']].round(2))
```

### Example 4: Visualize Trends

```python
import matplotlib.pyplot as plt

# Plot goals over seasons
plt.figure(figsize=(10, 6))
plt.plot(df['Season'], df['Gls'], marker='o', label='Goals')
plt.plot(df['Season'], df['Ast'], marker='s', label='Assists')
plt.xlabel('Season')
plt.ylabel('Count')
plt.title('Goals and Assists by Season')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('goals_assists_trend.png')
plt.show()
```

---

## 🔬 Step 5: Advanced Analysis Ideas

### Project Idea 1: Multi-Player Comparison

```python
import pandas as pd
import glob

# Load all player files
player_files = glob.glob('*_standard_stats.csv')

all_players = []
for file in player_files:
    df = pd.read_csv(file)
    player_name = file.replace('_standard_stats.csv', '').replace('_', ' ')
    df['Player'] = player_name
    all_players.append(df)

# Combine into one dataframe
comparison = pd.concat(all_players, ignore_index=True)

# Current season comparison
current = comparison[comparison['Season'] == '2025-2026']
current['G+A_per_90'] = current['G+A'] / current['90s']

# Top performers
top_performers = current.nlargest(10, 'G+A_per_90')
print(top_performers[['Player', 'Squad', 'Gls', 'Ast', 'G+A_per_90']])
```

### Project Idea 2: Position-Based Analysis

```python
# Load defensive actions
defensive = pd.read_csv('Kylian_Mbappe_defensive_actions.csv')

# Merge with standard stats
combined = pd.merge(
    df[['Season', '90s']], 
    defensive[['Season', 'Tkl', 'Int']], 
    on='Season'
)

# Calculate defensive actions per 90
combined['Tkl_per_90'] = combined['Tkl'] / combined['90s']
combined['Int_per_90'] = combined['Int'] / combined['90s']

print("Defensive contribution by season:")
print(combined[['Season', 'Tkl_per_90', 'Int_per_90']].round(2))
```

### Project Idea 3: Shot Efficiency

```python
# Load shooting stats
shooting = pd.read_csv('Kylian_Mbappe_shooting.csv')

# Analyze efficiency
shooting['Conversion_rate'] = shooting['Gls'] / shooting['Sh'] * 100
shooting['SoT_rate'] = shooting['SoT'] / shooting['Sh'] * 100

print("Shot efficiency by season:")
print(shooting[['Season', 'Sh', 'Gls', 'Conversion_rate', 'SoT_rate']])
```

---

## 📈 Step 6: Create Visualizations

### Visualization 1: Performance Dashboard

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Goals and Assists
axes[0, 0].bar(df['Season'], df['Gls'], alpha=0.7, label='Goals')
axes[0, 0].bar(df['Season'], df['Ast'], alpha=0.7, label='Assists')
axes[0, 0].set_title('Goals & Assists by Season')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: xG vs Actual
axes[0, 1].plot(df['Season'], df['Gls'], marker='o', label='Actual Goals')
axes[0, 1].plot(df['Season'], df['xG'], marker='s', label='Expected Goals')
axes[0, 1].set_title('Goals vs Expected Goals')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Minutes Played
axes[1, 0].bar(df['Season'], df['Min'])
axes[1, 0].set_title('Minutes Played by Season')
axes[1, 0].tick_params(axis='x', rotation=45)

# Plot 4: Progressive Actions
axes[1, 1].plot(df['Season'], df['PrgC'], marker='o', label='Progressive Carries')
axes[1, 1].plot(df['Season'], df['PrgP'], marker='s', label='Progressive Passes')
axes[1, 1].set_title('Progressive Actions')
axes[1, 1].legend()
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('performance_dashboard.png', dpi=300)
plt.show()
```

### Visualization 2: Heatmap

```python
import seaborn as sns

# Select key metrics
metrics = df[['Season', 'Gls', 'Ast', 'xG', 'npxG', 'xAG']].set_index('Season')

# Normalize for comparison
normalized = (metrics - metrics.min()) / (metrics.max() - metrics.min())

# Create heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(normalized.T, annot=True, fmt='.2f', cmap='RdYlGn', cbar_kws={'label': 'Normalized Value'})
plt.title('Performance Metrics Heatmap (Normalized)')
plt.xlabel('Season')
plt.ylabel('Metric')
plt.tight_layout()
plt.savefig('metrics_heatmap.png', dpi=300)
plt.show()
```

---

## 🎓 Step 7: Write Your Report

### Structure Your Analysis

**1. Introduction**
- Research question
- Why you chose these players/metrics
- Data source (cite FBref)

**2. Methodology**
```
Data was collected from FBref.com (Stats Perform Opta data) using 
responsible web scraping techniques with Python. Statistics were 
extracted for [X] players across [Y] seasons, focusing on domestic 
league performance.
```

**3. Results**
- Present your findings
- Include visualizations
- Compare metrics across players/seasons

**4. Discussion**
- Interpret the results
- What patterns did you find?
- Limitations of the analysis

**5. Conclusion**
- Summary of key findings
- Future research directions

### Citation Example

```
Data Source: FBref.com. "Kylian Mbappé Stats." 
<https://fbref.com/en/players/42fd9c7f/>. 
Powered by Stats Perform Opta. Accessed December 6, 2025.
```

---

## ✅ Checklist for Your Project

- [ ] Install Python and required packages
- [ ] Save HTML pages from FBref
- [ ] Run demo to test extraction
- [ ] Extract data for your chosen players
- [ ] Load data in pandas
- [ ] Calculate relevant metrics (per-90, efficiency, etc.)
- [ ] Create visualizations
- [ ] Compare across players/seasons
- [ ] Interpret findings
- [ ] Write report with proper citations
- [ ] Check your code runs without errors
- [ ] Comment your code for clarity

---

## 🐛 Common Issues and Solutions

### Issue 1: "Module not found"
**Solution**: Install missing package
```bash
pip install package_name
```

### Issue 2: "Empty dataframe"
**Problem**: Table not found in HTML
**Solution**: Check if that stats table exists for your player

### Issue 3: Encoding errors
**Solution**: Use UTF-8 encoding
```python
with open('file.html', 'r', encoding='utf-8') as f:
    html = f.read()
```

### Issue 4: Can't connect to FBref
**Solution**: Use saved HTML files instead of live scraping

---

## 📚 Additional Resources

### Python Tutorials
- **Pandas**: https://pandas.pydata.org/docs/getting_started/tutorials.html
- **Matplotlib**: https://matplotlib.org/stable/tutorials/index.html
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

### Football Analytics
- **FBref Glossary**: https://fbref.com/en/about/glossary.html
- **Expected Goals Explained**: Search for "xG explained" tutorials

### Web Scraping Ethics
- Always check robots.txt
- Respect rate limits
- Cache data locally
- Give proper attribution

---

## 🎉 Final Tips for Success

1. **Start Small**: Begin with 2-3 players, expand later
2. **Validate Data**: Check a few values manually against FBref
3. **Document Everything**: Comment your code as you go
4. **Save Often**: Keep backups of your scraped data
5. **Ask Questions**: If stuck, search for solutions online
6. **Have Fun**: Football + data = exciting analysis!

---

## 📧 Need Help?

Common resources:
- Python documentation
- Stack Overflow
- r/learnpython
- Your course instructor/TA

Remember: This is a learning project. Mistakes are part of the process!

Good luck with your project! ⚽📊🎓
