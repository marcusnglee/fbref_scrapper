"""
Split transfers_player_urls.json into 4 batches for parallel scraping
"""

import json
import math

def main():
    """Split player URLs into 4 equal batches"""

    print("="*60)
    print("Creating 4 Batches for Parallel Scraping")
    print("="*60)
    print()

    # Load all player URLs
    with open('transfers_player_urls.json', 'r', encoding='utf-8') as f:
        all_players = json.load(f)

    total = len(all_players)
    batch_size = math.ceil(total / 4)

    print(f"Total players: {total}")
    print(f"Batch size: ~{batch_size} players each")
    print()

    # Convert to list for easier splitting
    players_list = list(all_players.items())

    # Create 4 batches
    for i in range(4):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total)

        batch = dict(players_list[start_idx:end_idx])
        batch_file = f'batch_{i+1}_player_urls.json'

        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)

        print(f"✓ Batch {i+1}: {len(batch)} players → {batch_file}")

    print()
    print("="*60)
    print("Batches Created!")
    print("="*60)
    print()
    print("To scrape each batch, edit scrape_transfers_players.py")
    print("and change the input file, or run:")
    print()
    for i in range(1, 5):
        print(f"  # Batch {i}")
        print(f"  python3 scrape_batch.py batch_{i}_player_urls.json")
        print()

if __name__ == "__main__":
    main()
