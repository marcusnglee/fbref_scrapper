"""
Scrape a single batch of players
Usage: python3 scrape_batch.py batch_1_player_urls.json
"""

import json
import sys
from scrape_multiple_players import scrape_multiple_players

def main():
    """Load and scrape a batch of players"""

    if len(sys.argv) < 2:
        print("Usage: python3 scrape_batch.py <batch_file.json>")
        print("Example: python3 scrape_batch.py batch_1_player_urls.json")
        sys.exit(1)

    batch_file = sys.argv[1]

    print("="*60)
    print(f"Scraping Batch: {batch_file}")
    print("="*60)
    print()

    # Load batch
    try:
        with open(batch_file, 'r', encoding='utf-8') as f:
            player_urls = json.load(f)
    except FileNotFoundError:
        print(f"Error: {batch_file} not found!")
        print("Create batches first with: python3 create_batches.py")
        sys.exit(1)

    total_players = len(player_urls)
    print(f"Loaded {total_players} players from {batch_file}")
    print()

    # Estimate time
    delay = 15
    estimated_hours = (total_players * delay) / 3600
    print(f"Delay: {delay} seconds per player")
    print(f"Estimated time: ~{estimated_hours:.1f} hours ({estimated_hours*60:.0f} minutes)")
    print()
    print("Starting scrape...")
    print("Progress will be saved to outputs/ folder")
    print()

    # Scrape all players
    results = scrape_multiple_players(player_urls, delay=delay)

    print()
    print("="*60)
    print(f"BATCH {batch_file} COMPLETE!")
    print("="*60)
    print(f"Successfully scraped: {len(results)}/{total_players} players")
    print(f"Output location: outputs/ folder")
    print("="*60)


if __name__ == "__main__":
    main()
