"""
Extract player URLs from FBref player index for all unique players in transfers_1.csv
"""

import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import time
import logging
import json
import string
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import unicodedata
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PlayerURLFinder:
    """
    Extract player URLs from FBref by scraping the alphabetical player index
    and matching them to players in a CSV file
    """

    def __init__(self, csv_path: str, delay: int = 3, checkpoint_file: str = 'player_index_checkpoint.json'):
        """
        Initialize the PlayerURLFinder

        Args:
            csv_path: Path to transfers CSV file
            delay: Seconds to wait between requests (default: 3)
            checkpoint_file: File to save progress for resuming
        """
        self.csv_path = csv_path
        self.delay = delay
        self.checkpoint_file = checkpoint_file

        # Initialize cloudscraper (REQUIRED to bypass Cloudflare)
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )

        self.base_url = 'https://fbref.com'
        self.player_index_url = 'https://fbref.com/en/players/'

    def extract_unique_players_from_csv(self) -> List[str]:
        """
        Read CSV and extract unique player names

        Returns:
            Sorted list of unique player names
        """
        logger.info(f"Reading CSV file: {self.csv_path}")

        try:
            # Read CSV
            df = pd.read_csv(self.csv_path)

            # Check if Player column exists
            if 'Player' not in df.columns:
                raise ValueError("CSV must have a 'Player' column")

            # Extract unique players and remove any NaN values
            unique_players = df['Player'].dropna().unique().tolist()
            unique_players = sorted(unique_players)

            logger.info(f"Found {len(unique_players)} unique players in CSV")

            return unique_players

        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            raise

    def _normalize_name(self, name: str) -> str:
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

    def _generate_two_letter_combos(self) -> List[str]:
        """
        Generate all two-letter combinations (aa, ab, ..., zz)

        Returns:
            List of two-letter combinations
        """
        combos = []
        for first in string.ascii_lowercase:
            for second in string.ascii_lowercase:
                combos.append(f"{first}{second}")
        return combos

    def _get_required_combos(self, player_names: List[str]) -> List[str]:
        """
        Determine which two-letter combinations are needed based on player names
        This is MUCH more efficient than scraping all 676 combinations

        Args:
            player_names: List of player names from CSV

        Returns:
            Sorted list of unique two-letter combinations needed
        """
        required_combos = set()

        for name in player_names:
            # Normalize the name
            normalized = self._normalize_name(name)

            # Remove non-alphabetic characters from start
            cleaned = ''.join(c for c in normalized if c.isalpha())

            # Get first two letters
            if len(cleaned) >= 2:
                combo = cleaned[:2]
                required_combos.add(combo)
            elif len(cleaned) == 1:
                # If only one letter, we might need to check single letter pages
                # For now, skip these or we could try aa, ab, etc.
                logger.warning(f"Player name too short after normalization: {name}")

        sorted_combos = sorted(list(required_combos))
        logger.info(f"Need to scrape {len(sorted_combos)} letter combinations (instead of 676)")
        logger.info(f"This will save ~{(676 - len(sorted_combos)) * self.delay / 60:.1f} minutes!")

        return sorted_combos

    def _scrape_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Scrape a single page using cloudscraper

        Args:
            url: URL to scrape

        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            time.sleep(self.delay)
            logger.debug(f"Requesting: {url}")

            response = self.scraper.get(url, timeout=30)

            # Handle 404s (expected for non-existent letter combos)
            if response.status_code == 404:
                logger.debug(f"404 - Page not found: {url}")
                return None

            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')

        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            return None

    def _extract_players_from_page(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract player names and URLs from a player index page

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            Dictionary mapping player names to stats URLs
        """
        players = {}

        try:
            # Find all links that point to player pages
            for link in soup.find_all('a', href=True):
                href = link['href']

                # Player URLs have format: /en/players/{id}/{name}
                if '/players/' in href and href.count('/') >= 4:
                    # Skip if it's already a stats page or matchlog
                    if '-Stats' in href or 'matchlogs' in href:
                        continue

                    # Extract player name from link text
                    player_name = link.get_text(strip=True)

                    # Skip empty names or very short names (likely navigation links)
                    if not player_name or len(player_name) < 3:
                        continue

                    # Build stats URL
                    # href is like: /en/players/42fd9c7f/Kylian-Mbappe
                    # we need: https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats
                    if href.startswith('/'):
                        stats_url = f"{self.base_url}{href}-Stats"
                    else:
                        stats_url = f"{self.base_url}/{href}-Stats"

                    # Avoid duplicates (use original case for display)
                    if player_name not in players:
                        players[player_name] = stats_url

        except Exception as e:
            logger.error(f"Error extracting players from page: {e}")

        return players

    def scrape_player_index(self, resume: bool = True, target_combos: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Scrape the FBref player index across specified two-letter combinations

        Args:
            resume: If True, resume from checkpoint if it exists
            target_combos: If provided, only scrape these specific combos (SMART MODE)
                          If None, scrape all 676 combinations (not recommended)

        Returns:
            Dictionary mapping player names to their stats URLs
        """
        # Check for checkpoint
        all_players = {}
        processed_combos = set()

        if resume and os.path.exists(self.checkpoint_file):
            logger.info(f"Loading checkpoint from {self.checkpoint_file}")
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)
                all_players = checkpoint_data.get('players', {})
                processed_combos = set(checkpoint_data.get('processed_combos', []))
            logger.info(f"Resuming with {len(all_players)} players and {len(processed_combos)} combos processed")

        # Determine which combinations to scrape
        if target_combos is not None:
            combos = target_combos
            logger.info("SMART MODE: Only scraping needed letter combinations")
        else:
            combos = self._generate_two_letter_combos()
            logger.warning("Scraping ALL combinations - this may trigger rate limits!")

        remaining_combos = [c for c in combos if c not in processed_combos]

        logger.info(f"Starting to scrape player index")
        logger.info(f"Total combinations to process: {len(remaining_combos)}")
        logger.info(f"Estimated time: ~{len(remaining_combos) * self.delay / 60:.1f} minutes")

        start_time = time.time()

        for idx, combo in enumerate(remaining_combos, 1):
            url = f"{self.player_index_url}{combo}/"

            logger.info(f"[{idx}/{len(remaining_combos)}] Scraping: {combo} ({len(all_players)} players found so far)")

            soup = self._scrape_page(url)

            if soup:
                players_on_page = self._extract_players_from_page(soup)
                all_players.update(players_on_page)
                logger.info(f"  Found {len(players_on_page)} players on this page")

            processed_combos.add(combo)

            # Save checkpoint every 50 pages
            if idx % 50 == 0:
                self._save_checkpoint(all_players, list(processed_combos))
                elapsed = time.time() - start_time
                rate = idx / elapsed
                remaining_time = (len(remaining_combos) - idx) / rate
                logger.info(f"  Checkpoint saved. ETA: {remaining_time / 60:.1f} minutes")

        # Final save
        self._save_checkpoint(all_players, list(processed_combos))

        elapsed_time = time.time() - start_time
        logger.info(f"Scraping complete! Total players found: {len(all_players)}")
        logger.info(f"Time taken: {elapsed_time / 60:.1f} minutes")

        return all_players

    def _save_checkpoint(self, players: Dict[str, str], processed_combos: List[str]):
        """Save checkpoint data"""
        checkpoint_data = {
            'players': players,
            'processed_combos': processed_combos,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)

        logger.debug(f"Checkpoint saved: {len(players)} players, {len(processed_combos)} combos")

    def match_players(self, csv_players: List[str], index_players: Dict[str, str]) -> Tuple[Dict[str, str], List[str]]:
        """
        Match players from CSV to the scraped player index

        Args:
            csv_players: List of player names from CSV
            index_players: Dictionary of player names to URLs from index

        Returns:
            Tuple of (matched_dict, unmatched_list)
        """
        logger.info("Matching CSV players to scraped index...")

        # Create normalized lookup dictionary
        normalized_index = {
            self._normalize_name(name): (name, url)
            for name, url in index_players.items()
        }

        matched = {}
        unmatched = []

        for csv_name in csv_players:
            normalized_csv = self._normalize_name(csv_name)

            if normalized_csv in normalized_index:
                original_name, url = normalized_index[normalized_csv]
                matched[csv_name] = url
                logger.debug(f"Matched: {csv_name} -> {original_name}")
            else:
                unmatched.append(csv_name)
                logger.debug(f"Not found: {csv_name}")

        logger.info(f"Matching complete: {len(matched)} matched, {len(unmatched)} not found")

        return matched, unmatched

    def save_results(self, matched: Dict[str, str], unmatched: List[str],
                     output_dir: str = '.'):
        """
        Save results to files

        Args:
            matched: Dictionary of matched players and URLs
            unmatched: List of unmatched player names
            output_dir: Directory to save output files
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save matched players to JSON
        matched_file = os.path.join(output_dir, 'player_urls.json')
        with open(matched_file, 'w', encoding='utf-8') as f:
            json.dump(matched, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(matched)} matched URLs to: {matched_file}")

        # Save unmatched players to text file
        unmatched_file = os.path.join(output_dir, 'unmatched_players.txt')
        with open(unmatched_file, 'w', encoding='utf-8') as f:
            for name in sorted(unmatched):
                f.write(f"{name}\n")
        logger.info(f"Saved {len(unmatched)} unmatched players to: {unmatched_file}")

        # Generate and save summary report
        summary_file = os.path.join(output_dir, 'player_url_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("Player URL Extraction Summary\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"CSV File: {self.csv_path}\n\n")

            f.write(f"Total unique players in CSV: {len(matched) + len(unmatched)}\n")
            f.write(f"Successfully matched: {len(matched)} ({len(matched)/(len(matched)+len(unmatched))*100:.1f}%)\n")
            f.write(f"Not found: {len(unmatched)} ({len(unmatched)/(len(matched)+len(unmatched))*100:.1f}%)\n\n")

            f.write("Sample matched URLs (first 10):\n")
            f.write("-" * 60 + "\n")
            for name, url in list(matched.items())[:10]:
                f.write(f"{name}\n  -> {url}\n")

        logger.info(f"Saved summary to: {summary_file}")

        print(f"\n{'='*60}")
        print("Results saved successfully!")
        print(f"{'='*60}")
        print(f"Matched players: {matched_file}")
        print(f"Unmatched players: {unmatched_file}")
        print(f"Summary report: {summary_file}")
        print(f"{'='*60}\n")

    def run(self, resume: bool = True, smart_mode: bool = True):
        """
        Main workflow: extract players, scrape index, match, and save

        Args:
            resume: Resume from checkpoint if available
            smart_mode: If True, only scrape needed letter combos (recommended)
        """
        print("="*60)
        print("FBref Player URL Finder - SMART MODE")
        print("="*60)
        print()

        # Step 1: Extract unique players from CSV
        print("Step 1: Extracting unique players from CSV...")
        csv_players = self.extract_unique_players_from_csv()
        print(f"  Found {len(csv_players)} unique players\n")

        # Step 1.5: Determine required letter combinations (SMART MODE)
        required_combos = None
        if smart_mode:
            print("Step 1.5: Analyzing which letter combinations are needed...")
            required_combos = self._get_required_combos(csv_players)
            print(f"  Need to scrape only {len(required_combos)} combinations")
            print(f"  Estimated time: ~{len(required_combos) * self.delay / 60:.1f} minutes\n")
        else:
            print("  WARNING: Smart mode disabled - will scrape all 676 combinations\n")

        # Step 2: Scrape player index
        print("Step 2: Scraping FBref player index...")
        print(f"  Progress will be checkpointed every 50 pages\n")

        index_players = self.scrape_player_index(resume=resume, target_combos=required_combos)
        print(f"  Scraped {len(index_players)} total players from index\n")

        # Step 3: Match players
        print("Step 3: Matching CSV players to index...")
        matched, unmatched = self.match_players(csv_players, index_players)
        print(f"  Matched: {len(matched)}")
        print(f"  Not found: {len(unmatched)}\n")

        # Step 4: Save results
        print("Step 4: Saving results...")
        self.save_results(matched, unmatched)

        print("\n" + "="*60)
        print("COMPLETE!")
        print("="*60)
        print(f"\nYou can now use player_urls.json with scrape_multiple_players.py")
        print(f"to scrape stats for all {len(matched)} matched players.\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract FBref player URLs for players in a CSV file (SMART MODE)'
    )
    parser.add_argument(
        '--csv',
        default='transfers_1.csv',
        help='Path to CSV file with Player column (default: transfers_1.csv)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=8,
        help='Delay between requests in seconds (default: 8, recommended for rate limit avoidance)'
    )
    parser.add_argument(
        '--no-resume',
        action='store_true',
        help='Start fresh, ignoring any existing checkpoint'
    )
    parser.add_argument(
        '--no-smart-mode',
        action='store_true',
        help='Disable smart mode and scrape all 676 letter combinations (not recommended)'
    )

    args = parser.parse_args()

    # Create finder and run
    finder = PlayerURLFinder(
        csv_path=args.csv,
        delay=args.delay
    )

    finder.run(resume=not args.no_resume, smart_mode=not args.no_smart_mode)


if __name__ == "__main__":
    main()
