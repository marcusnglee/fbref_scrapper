"""
Complete workflow: Get player URLs from a team and scrape their stats
"""
from get_player_urls import get_player_urls_from_squad, save_urls_to_file
from scrape_multiple_players import scrape_multiple_players
import json
import time


def scrape_entire_team(team_url, team_name, delay=8):
    """
    Complete workflow to scrape all players from a team

    Args:
        team_url: URL to team's squad page
        team_name: Name for saving files
        delay: Delay between requests (seconds)
    """
    print(f"\n{'='*60}")
    print(f"Scraping Workflow: {team_name}")
    print(f"{'='*60}\n")

    # Step 1: Get player URLs
    print("Step 1: Extracting player URLs from squad page...")
    player_urls = get_player_urls_from_squad(team_url, delay=3)

    # Filter out any problematic entries
    filtered_urls = {k: v for k, v in player_urls.items()
                     if '-Stats' in v and 'matchlogs' not in v}

    print(f"Found {len(filtered_urls)} valid player URLs\n")

    # Save URLs to file
    urls_filename = f"{team_name.replace(' ', '_')}_urls.json"
    save_urls_to_file(filtered_urls, urls_filename)

    # Step 2: Ask user if they want to proceed
    print(f"\n{'='*60}")
    print(f"Ready to scrape {len(filtered_urls)} players")
    print(f"This will take approximately {len(filtered_urls) * delay / 60:.1f} minutes")
    print(f"{'='*60}\n")

    response = input("Do you want to proceed? (yes/no): ").strip().lower()

    if response != 'yes':
        print("Scraping cancelled. URLs saved to:", urls_filename)
        return None

    # Step 3: Scrape all players
    print(f"\nStep 2: Scraping player stats...")
    results = scrape_multiple_players(filtered_urls, delay=delay)

    print(f"\n{'='*60}")
    print(f"Workflow Complete!")
    print(f"Scraped {len(results)}/{len(filtered_urls)} players successfully")
    print(f"{'='*60}\n")

    return results


def scrape_from_saved_urls(json_file, delay=8):
    """
    Scrape players from a saved JSON file of URLs

    Args:
        json_file: Path to JSON file with player URLs
        delay: Delay between requests
    """
    print(f"Loading player URLs from {json_file}...")

    with open(json_file, 'r', encoding='utf-8') as f:
        player_urls = json.load(f)

    print(f"Found {len(player_urls)} players")

    results = scrape_multiple_players(player_urls, delay=delay)

    return results


if __name__ == "__main__":
    # Example usage options:

    # Option 1: Scrape an entire team
    print("\nOption 1: Scrape entire team (Real Madrid)")
    print("="*60)

    real_madrid_url = "https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
    scrape_entire_team(real_madrid_url, "Real Madrid", delay=8)

    # Option 2: Other popular teams
    # Uncomment to use:

    # Manchester City
    # man_city_url = "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
    # scrape_entire_team(man_city_url, "Manchester City", delay=8)

    # Barcelona
    # barca_url = "https://fbref.com/en/squads/206d90db/Barcelona-Stats"
    # scrape_entire_team(barca_url, "Barcelona", delay=8)

    # Bayern Munich
    # bayern_url = "https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats"
    # scrape_entire_team(bayern_url, "Bayern Munich", delay=8)

    # Paris Saint-Germain
    # psg_url = "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats"
    # scrape_entire_team(psg_url, "PSG", delay=8)

    # Liverpool
    # liverpool_url = "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats"
    # scrape_entire_team(liverpool_url, "Liverpool", delay=8)


    # Option 3: Scrape from previously saved URLs
    # Uncomment to use:
    # results = scrape_from_saved_urls('real_madrid_players.json', delay=8)
