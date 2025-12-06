"""
Script to scrape multiple players from FBref
"""
from fbref_scraper import FBrefScraper
import time

def scrape_multiple_players(player_urls, delay=5):
    """
    Scrape stats for multiple players

    Args:
        player_urls: List of player URLs or dict with player names as keys
        delay: Seconds to wait between requests (default: 5)
    """
    scraper = FBrefScraper(delay=delay)
    results_collection = {}

    # Handle both list and dict inputs
    if isinstance(player_urls, dict):
        players = player_urls
    else:
        players = {f"Player_{i}": url for i, url in enumerate(player_urls)}

    total = len(players)
    print(f"\n{'='*60}")
    print(f"Starting scrape for {total} players")
    print(f"{'='*60}\n")

    for idx, (name, url) in enumerate(players.items(), 1):
        print(f"[{idx}/{total}] Scraping: {name}")
        print(f"URL: {url}")

        try:
            results = scraper.scrape_player_stats(url)

            if results:
                # Save results immediately
                scraper.save_results(results)
                results_collection[name] = results

                player_name = results.get('player_info', {}).get('player_name', name)
                tables_count = len([k for k, v in results.items() if isinstance(v, dict) or hasattr(v, 'shape')])
                print(f"✓ Success! Extracted {tables_count} tables for {player_name}")
            else:
                print(f"✗ Failed to scrape {name}")

        except Exception as e:
            print(f"✗ Error scraping {name}: {e}")

        # Add extra delay between players
        if idx < total:
            print(f"Waiting {delay} seconds before next player...\n")
            time.sleep(delay)

    print(f"\n{'='*60}")
    print(f"Scraping Complete!")
    print(f"Successfully scraped: {len(results_collection)}/{total} players")
    print(f"{'='*60}\n")

    return results_collection


if __name__ == "__main__":
    # Example: Top players to scrape
    players = {
        "Kylian Mbappé": "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats",
        "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
        "Mohamed Salah": "https://fbref.com/en/players/e342ad68/Mohamed-Salah-Stats",
        "Vinicius Jr": "https://fbref.com/en/players/5ade27f0/Vinicius-Junior-Stats",
        # Add more players here...
    }

    # Scrape all players
    results = scrape_multiple_players(players, delay=5)

    print(f"\nAll player data saved to 'outputs/' folder")
    print(f"Each player has:")
    print(f"  - Individual CSV files for each stats table")
    print(f"  - Combined Excel workbook with all tables")
    print(f"  - JSON file with player metadata")
