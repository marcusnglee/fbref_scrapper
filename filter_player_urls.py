"""
Filter player_urls.json to only include players from transfers_1.csv
"""

import pandas as pd
import json
import unicodedata
from typing import Dict, List


def normalize_name(name: str) -> str:
    """
    Normalize player name for matching (lowercase, remove accents)

    Args:
        name: Player name

    Returns:
        Normalized name
    """
    # Convert to lowercase
    name = name.lower()

    # Remove accents/diacritics
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # Remove extra whitespace
    name = ' '.join(name.split())

    return name


def extract_unique_players_from_csv(csv_path: str) -> List[str]:
    """
    Read CSV and extract unique player names

    Args:
        csv_path: Path to CSV file

    Returns:
        Sorted list of unique player names
    """
    print(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)

    if 'Player' not in df.columns:
        raise ValueError("CSV must have a 'Player' column")

    unique_players = df['Player'].dropna().unique().tolist()
    unique_players = sorted(unique_players)

    print(f"Found {len(unique_players)} unique players in CSV")
    return unique_players


def load_player_urls(json_path: str) -> Dict[str, str]:
    """
    Load player URLs from JSON file

    Args:
        json_path: Path to JSON file with all player URLs

    Returns:
        Dictionary of player name -> URL
    """
    print(f"Loading player URLs from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        player_urls = json.load(f)

    print(f"Loaded {len(player_urls)} total player URLs")
    return player_urls


def match_and_filter(csv_players: List[str], all_urls: Dict[str, str]) -> tuple[Dict[str, str], List[str]]:
    """
    Match CSV players to the full URL database and create filtered list

    Args:
        csv_players: List of player names from CSV
        all_urls: Dictionary of all player URLs

    Returns:
        Tuple of (matched_dict, unmatched_list)
    """
    print("\nMatching players...")

    # Create normalized lookup dictionary
    normalized_index = {
        normalize_name(name): (name, url)
        for name, url in all_urls.items()
    }

    matched = {}
    unmatched = []

    for csv_name in csv_players:
        normalized_csv = normalize_name(csv_name)

        if normalized_csv in normalized_index:
            original_name, url = normalized_index[normalized_csv]
            matched[csv_name] = url
        else:
            unmatched.append(csv_name)

    print(f"\nMatching complete:")
    print(f"  ✓ Matched: {len(matched)} ({len(matched)/(len(csv_players))*100:.1f}%)")
    print(f"  ✗ Not found: {len(unmatched)} ({len(unmatched)/(len(csv_players))*100:.1f}%)")

    return matched, unmatched


def save_results(matched: Dict[str, str], unmatched: List[str]):
    """
    Save filtered URLs and unmatched players

    Args:
        matched: Dictionary of matched player URLs
        unmatched: List of unmatched player names
    """
    # Save filtered URLs
    filtered_file = 'transfers_player_urls.json'
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump(matched, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved filtered URLs to: {filtered_file}")

    # Save unmatched players
    if unmatched:
        unmatched_file = 'transfers_unmatched_players.txt'
        with open(unmatched_file, 'w', encoding='utf-8') as f:
            for name in sorted(unmatched):
                f.write(f"{name}\n")
        print(f"✓ Saved {len(unmatched)} unmatched players to: {unmatched_file}")

    # Save summary
    summary_file = 'transfers_url_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("Filtered Player URLs Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Source CSV: transfers_1.csv\n")
        f.write(f"Total unique players: {len(matched) + len(unmatched)}\n")
        f.write(f"Matched: {len(matched)}\n")
        f.write(f"Not found: {len(unmatched)}\n\n")

        f.write("Sample matched URLs (first 10):\n")
        f.write("-" * 60 + "\n")
        for name, url in list(matched.items())[:10]:
            f.write(f"{name}\n  -> {url}\n\n")

    print(f"✓ Saved summary to: {summary_file}")


def main():
    """Main function"""
    print("="*60)
    print("Filter Player URLs for transfers_1.csv")
    print("="*60)
    print()

    # Step 1: Extract unique players from CSV
    csv_players = extract_unique_players_from_csv('transfers_1.csv')

    # Step 2: Load all player URLs
    all_urls = load_player_urls('player_urls.json')

    # Step 3: Match and filter
    matched, unmatched = match_and_filter(csv_players, all_urls)

    # Step 4: Save results
    save_results(matched, unmatched)

    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60)
    print(f"\nFiltered player URLs saved to: transfers_player_urls.json")
    print(f"Ready to use with scrape_multiple_players.py\n")


if __name__ == "__main__":
    main()
