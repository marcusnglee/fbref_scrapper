"""
Utility to extract player URLs from FBref team or league pages
"""
import cloudscraper
from bs4 import BeautifulSoup
import time
import json


def get_player_urls_from_squad(squad_url, delay=3):
    """
    Extract all player URLs from a team/squad page

    Args:
        squad_url: URL to a team's squad page on FBref
        delay: Delay before making request

    Returns:
        Dictionary with player names as keys and URLs as values
    """
    print(f"Fetching squad page: {squad_url}")

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )

    time.sleep(delay)
    response = scraper.get(squad_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all player links
    player_urls = {}

    # Look for links to player pages (they contain '/players/' in the URL)
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/players/' in href and '-Stats' not in href:
            # Construct the stats page URL
            player_id = href.split('/players/')[1].split('/')[0]
            player_name_slug = href.split('/players/')[1].split('/')[1] if '/' in href.split('/players/')[1] else None

            if player_name_slug:
                player_name = link.get_text(strip=True)
                stats_url = f"https://fbref.com/en/players/{player_id}/{player_name_slug}-Stats"

                # Filter out non-player links and avoid duplicates
                skip_terms = ['Matches', 'matchlogs', 'all_comps']
                if player_name and player_name not in player_urls:
                    if not any(term in stats_url for term in skip_terms):
                        player_urls[player_name] = stats_url

    print(f"Found {len(player_urls)} players")
    return player_urls


def get_player_urls_from_league_stats(league_stats_url, delay=3):
    """
    Extract player URLs from a league's player stats table

    Args:
        league_stats_url: URL to league player stats page
        delay: Delay before request

    Returns:
        Dictionary with player names as keys and URLs as values
    """
    print(f"Fetching league stats page: {league_stats_url}")

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )

    time.sleep(delay)
    response = scraper.get(league_stats_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    player_urls = {}

    # Find player stats table
    stats_table = soup.find('table', {'id': 'stats_standard'})

    if stats_table:
        # Find all player links in the table
        for row in stats_table.find_all('tr'):
            player_cell = row.find('th', {'data-stat': 'player'})
            if player_cell:
                link = player_cell.find('a', href=True)
                if link and '/players/' in link['href']:
                    player_name = link.get_text(strip=True)
                    # Convert relative URL to absolute
                    player_url = f"https://fbref.com{link['href']}"

                    if player_name not in player_urls:
                        player_urls[player_name] = player_url

    print(f"Found {len(player_urls)} players")
    return player_urls


def save_urls_to_file(player_urls, filename='player_urls.json'):
    """Save player URLs to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(player_urls, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(player_urls)} player URLs to {filename}")


if __name__ == "__main__":
    # Example 1: Get all players from a team's squad page
    print("="*60)
    print("Example 1: Real Madrid Squad")
    print("="*60)

    real_madrid_url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
    players = get_player_urls_from_squad(real_madrid_url, delay=3)

    # Display first 10 players
    print("\nFirst 10 players found:")
    for i, (name, url) in enumerate(list(players.items())[:10], 1):
        print(f"{i}. {name}")
        print(f"   {url}\n")

    # Save to file
    save_urls_to_file(players, 'real_madrid_players.json')

    print(f"\n{'='*60}")
    print("You can now use these URLs with scrape_multiple_players.py")
    print(f"{'='*60}")

    # Example 2: Premier League top scorers
    # Uncomment to use:
    # print("\n" + "="*60)
    # print("Example 2: Premier League Stats")
    # print("="*60)
    # prem_url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    # prem_players = get_player_urls_from_league_stats(prem_url, delay=5)
    # save_urls_to_file(prem_players, 'premier_league_players.json')
