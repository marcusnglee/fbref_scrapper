# FBref Team URLs Reference

## How to Find Team URLs

1. Go to [fbref.com](https://fbref.com)
2. Navigate to the league/competition
3. Click on a team
4. Copy the URL from the browser
5. Format: `https://fbref.com/en/squads/{team_id}/{Team-Name}-Stats`

## Premier League (England)

```python
premier_league_teams = {
    "Manchester City": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "Arsenal": "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "Chelsea": "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
    "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "Tottenham": "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
    "Newcastle": "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
    "Aston Villa": "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
}
```

## La Liga (Spain)

```python
la_liga_teams = {
    "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats",
    "Barcelona": "https://fbref.com/en/squads/206d90db/Barcelona-Stats",
    "Atlético Madrid": "https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats",
    "Athletic Club": "https://fbref.com/en/squads/2b390eca/Athletic-Club-Stats",
    "Real Sociedad": "https://fbref.com/en/squads/e31d1cd9/Real-Sociedad-Stats",
    "Villarreal": "https://fbref.com/en/squads/2a8183b3/Villarreal-Stats",
    "Sevilla": "https://fbref.com/en/squads/ad2be733/Sevilla-Stats",
}
```

## Serie A (Italy)

```python
serie_a_teams = {
    "Inter": "https://fbref.com/en/squads/d609edc0/Inter-Stats",
    "AC Milan": "https://fbref.com/en/squads/c07e2619/AC-Milan-Stats",
    "Juventus": "https://fbref.com/en/squads/e0652b02/Juventus-Stats",
    "Napoli": "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats",
    "Roma": "https://fbref.com/en/squads/cf74a709/Roma-Stats",
    "Lazio": "https://fbref.com/en/squads/7213da33/Lazio-Stats",
    "Atalanta": "https://fbref.com/en/squads/922493e3/Atalanta-Stats",
}
```

## Bundesliga (Germany)

```python
bundesliga_teams = {
    "Bayern Munich": "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats",
    "Borussia Dortmund": "https://fbref.com/en/squads/add600ae/Borussia-Dortmund-Stats",
    "RB Leipzig": "https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats",
    "Bayer Leverkusen": "https://fbref.com/en/squads/c7a9f859/Bayer-Leverkusen-Stats",
    "Union Berlin": "https://fbref.com/en/squads/91eef634/Union-Berlin-Stats",
    "Eintracht Frankfurt": "https://fbref.com/en/squads/f0ac8ee6/Eintracht-Frankfurt-Stats",
}
```

## Ligue 1 (France)

```python
ligue_1_teams = {
    "Paris Saint-Germain": "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats",
    "Monaco": "https://fbref.com/en/squads/fd6114db/Monaco-Stats",
    "Marseille": "https://fbref.com/en/squads/5725cc7b/Marseille-Stats",
    "Lyon": "https://fbref.com/en/squads/341c8c03/Lyon-Stats",
    "Lille": "https://fbref.com/en/squads/cb188c0e/Lille-Stats",
}
```

## How to Use These URLs

### Get Player URLs from Multiple Teams

```python
from get_player_urls import get_player_urls_from_squad, save_urls_to_file
import time

teams = {
    "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats",
    "Barcelona": "https://fbref.com/en/squads/206d90db/Barcelona-Stats",
}

all_players = {}

for team_name, team_url in teams.items():
    print(f"Getting players from {team_name}...")
    players = get_player_urls_from_squad(team_url, delay=5)
    all_players.update(players)
    time.sleep(10)  # Wait between teams

save_urls_to_file(all_players, 'la_liga_top_teams.json')
print(f"Total players: {len(all_players)}")
```

### Scrape Specific Positions

If you only want certain players, manually create a list:

```python
top_strikers = {
    "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
    "Kylian Mbappé": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats",
    "Harry Kane": "https://fbref.com/en/players/21a66f6a/Harry-Kane-Stats",
    "Robert Lewandowski": "https://fbref.com/en/players/a5d3ce24/Robert-Lewandowski-Stats",
    "Victor Osimhen": "https://fbref.com/en/players/b5e599cc/Victor-Osimhen-Stats",
}

from scrape_multiple_players import scrape_multiple_players
results = scrape_multiple_players(top_strikers, delay=8)
```

## Finding Individual Player URLs

### Method 1: Search on FBref
1. Go to fbref.com
2. Use search box (top right)
3. Type player name
4. Click on player
5. Copy URL

### Method 2: Pattern Recognition
URLs follow this pattern:
```
https://fbref.com/en/players/{8-char-id}/{Player-Name}-Stats
```

Examples:
- Mbappé: `42fd9c7f/Kylian-Mbappe-Stats`
- Haaland: `1f44ac21/Erling-Haaland-Stats`
- Salah: `e342ad68/Mohamed-Salah-Stats`

## League Stats Pages

To get top scorers/players from entire leagues:

```python
from get_player_urls import get_player_urls_from_league_stats

# Premier League
prem_url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
players = get_player_urls_from_league_stats(prem_url)

# La Liga
la_liga_url = "https://fbref.com/en/comps/12/stats/La-Liga-Stats"

# Serie A
serie_a_url = "https://fbref.com/en/comps/11/stats/Serie-A-Stats"

# Bundesliga
bundesliga_url = "https://fbref.com/en/comps/20/stats/Bundesliga-Stats"

# Ligue 1
ligue1_url = "https://fbref.com/en/comps/13/stats/Ligue-1-Stats"
```

## Tips

1. **Save URLs first**: Always save player URLs to JSON before scraping
2. **Check before scraping**: Review the JSON file to verify you have the right players
3. **Batch processing**: Don't scrape 100+ players at once - break into batches
4. **Conservative delays**: Use 8-10 second delays for large batches
