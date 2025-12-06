"""
Complete Example: Get URLs and Scrape Players
Choose your method and run this script
"""
from get_player_urls import get_player_urls_from_squad, get_player_urls_from_league_stats, save_urls_to_file
from scrape_multiple_players import scrape_multiple_players
import json
import os


def example_1_single_team():
    """Example 1: Scrape all players from a single team"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Scrape Real Madrid Squad")
    print("="*60 + "\n")

    # Get player URLs
    team_url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
    players = get_player_urls_from_squad(team_url, delay=3)

    # Save URLs
    save_urls_to_file(players, 'real_madrid_players.json')

    # Scrape all players
    print(f"\nScraping {len(players)} players...")
    results = scrape_multiple_players(players, delay=8)

    print(f"\n✓ Complete! Scraped {len(results)} players")
    print("Check the 'outputs/' folder for CSV files\n")


def example_2_multiple_teams():
    """Example 2: Get URLs from multiple teams"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Get URLs from La Liga Top 3 Teams")
    print("="*60 + "\n")

    teams = {
        "Real Madrid": "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats",
        "Barcelona": "https://fbref.com/en/squads/206d90db/Barcelona-Stats",
        "Atlético Madrid": "https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats",
    }

    all_players = {}

    for team_name, team_url in teams.items():
        print(f"Getting players from {team_name}...")
        players = get_player_urls_from_squad(team_url, delay=3)
        all_players.update(players)
        print(f"  Found {len(players)} players\n")

        # Small delay between teams
        import time
        time.sleep(5)

    print(f"Total players: {len(all_players)}")

    # Save all URLs
    save_urls_to_file(all_players, 'la_liga_top3.json')

    # Ask before scraping
    response = input(f"\nScrape all {len(all_players)} players? (yes/no): ")
    if response.lower() == 'yes':
        results = scrape_multiple_players(all_players, delay=8)
        print(f"\n✓ Complete! Scraped {len(results)} players")


def example_3_league_stats():
    """Example 3: Get top players from a league"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Get Premier League Top Players")
    print("="*60 + "\n")

    # Get players from league stats page
    league_url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    players = get_player_urls_from_league_stats(league_url, delay=3)

    # Save URLs
    save_urls_to_file(players, 'premier_league_players.json')

    print(f"\nFound {len(players)} players from Premier League")
    print("URLs saved to 'premier_league_players.json'")

    # Scrape first 10 for testing
    test_players = dict(list(players.items())[:10])

    response = input(f"\nScrape first 10 players as a test? (yes/no): ")
    if response.lower() == 'yes':
        results = scrape_multiple_players(test_players, delay=8)
        print(f"\n✓ Complete! Scraped {len(results)} players")


def example_4_manual_list():
    """Example 4: Manually create list of top strikers"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Top Strikers Manual List")
    print("="*60 + "\n")

    top_strikers = {
        "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
        "Kylian Mbappé": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats",
        "Harry Kane": "https://fbref.com/en/players/21a66f6a/Harry-Kane-Stats",
        "Mohamed Salah": "https://fbref.com/en/players/e342ad68/Mohamed-Salah-Stats",
        "Robert Lewandowski": "https://fbref.com/en/players/a5d3ce24/Robert-Lewandowski-Stats",
    }

    # Save to JSON
    with open('top_strikers.json', 'w') as f:
        json.dump(top_strikers, f, indent=2)

    print(f"Created list of {len(top_strikers)} top strikers")
    print("URLs saved to 'top_strikers.json'\n")

    # Scrape
    response = input(f"Scrape all {len(top_strikers)} strikers? (yes/no): ")
    if response.lower() == 'yes':
        results = scrape_multiple_players(top_strikers, delay=8)
        print(f"\n✓ Complete! Scraped {len(results)} players")


def example_5_resume_scraping():
    """Example 5: Resume from saved JSON file"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Resume Scraping from Saved URLs")
    print("="*60 + "\n")

    json_files = [f for f in os.listdir('.') if f.endswith('_players.json')]

    if not json_files:
        print("No saved player URL files found.")
        print("Run one of the other examples first to create a JSON file.\n")
        return

    print("Available player URL files:")
    for i, file in enumerate(json_files, 1):
        with open(file, 'r') as f:
            data = json.load(f)
        print(f"{i}. {file} ({len(data)} players)")

    choice = input("\nEnter file number to scrape (or 'q' to quit): ")

    if choice.lower() == 'q':
        return

    try:
        selected_file = json_files[int(choice) - 1]
        with open(selected_file, 'r') as f:
            players = json.load(f)

        print(f"\nLoaded {len(players)} players from {selected_file}")

        results = scrape_multiple_players(players, delay=8)
        print(f"\n✓ Complete! Scraped {len(results)} players")

    except (ValueError, IndexError):
        print("Invalid choice")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FBref Scraper - Complete Workflow Examples")
    print("="*60)

    examples = {
        "1": ("Scrape single team (Real Madrid)", example_1_single_team),
        "2": ("Get URLs from multiple teams", example_2_multiple_teams),
        "3": ("Get top players from a league", example_3_league_stats),
        "4": ("Manual list of top strikers", example_4_manual_list),
        "5": ("Resume from saved JSON file", example_5_resume_scraping),
    }

    print("\nChoose an example:")
    for key, (description, _) in examples.items():
        print(f"{key}. {description}")

    print("q. Quit")

    choice = input("\nYour choice: ").strip()

    if choice in examples:
        examples[choice][1]()
    elif choice.lower() == 'q':
        print("Goodbye!")
    else:
        print("Invalid choice")
