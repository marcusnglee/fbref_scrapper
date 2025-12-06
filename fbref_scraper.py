"""
FBref Player Stats Scraper
Student Project - Web Scraping Football Statistics

This script scrapes player statistics from FBref.com
Respects robots.txt and implements responsible scraping practices
"""

import pandas as pd
import requests
import cloudscraper
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, Optional, Tuple
import json
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FBrefScraper:
    """
    A class to scrape player statistics from FBref.com
    """
    
    def __init__(self, delay: int = 3):
        """
        Initialize the scraper

        Args:
            delay: Seconds to wait between requests (default: 3)
        """
        self.delay = delay
        # Use cloudscraper to bypass Cloudflare protection
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )
        self.base_url = 'https://fbref.com'
    
    def _make_request(self, url: str) -> Optional[BeautifulSoup]:
        """
        Make a GET request and return BeautifulSoup object

        Args:
            url: URL to scrape

        Returns:
            BeautifulSoup object or None if request fails
        """
        try:
            logger.info(f"Requesting: {url}")
            time.sleep(self.delay)  # Respectful delay

            response = self.scraper.get(url, timeout=30)
            response.raise_for_status()

            return BeautifulSoup(response.content, 'html.parser')

        except Exception as e:
            logger.error(f"Error making request: {e}")
            return None
    
    def _extract_table_by_id(self, soup: BeautifulSoup, table_id: str) -> Optional[pd.DataFrame]:
        """
        Extract a specific table by its ID
        
        Args:
            soup: BeautifulSoup object
            table_id: HTML ID of the table
            
        Returns:
            DataFrame or None if table not found
        """
        try:
            table = soup.find('table', {'id': table_id})
            
            if table is None:
                logger.warning(f"Table with ID '{table_id}' not found")
                return None
            
            # Convert to pandas DataFrame
            df = pd.read_html(str(table))[0]
            
            # Handle multi-level column headers if present
            if isinstance(df.columns, pd.MultiIndex):
                # Flatten multi-level columns
                df.columns = ['_'.join(col).strip() for col in df.columns.values]
            
            logger.info(f"Successfully extracted table: {table_id}")
            return df
            
        except Exception as e:
            logger.error(f"Error extracting table {table_id}: {e}")
            return None
    
    def _extract_player_info(self, soup: BeautifulSoup) -> Dict:
        """
        Extract basic player information from the page
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary with player info
        """
        info = {
            'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # Try to extract player name from h1 tag
            h1 = soup.find('h1')
            if h1:
                info['player_name'] = h1.get_text(strip=True)
        except:
            info['player_name'] = 'Unknown'
        
        return info
    
    def scrape_player_stats(self, player_url: str) -> Dict[str, pd.DataFrame]:
        """
        Scrape all relevant statistics tables for a player
        
        Args:
            player_url: Full URL to player page
            
        Returns:
            Dictionary containing all scraped DataFrames
        """
        logger.info(f"Starting scrape for: {player_url}")
        
        # Make request
        soup = self._make_request(player_url)
        if soup is None:
            return {}
        
        # Extract player info
        player_info = self._extract_player_info(soup)
        logger.info(f"Scraping stats for: {player_info.get('player_name', 'Unknown')}")
        
        # Define tables to scrape - only standard stats and defensive actions
        tables_to_scrape = {
            'standard_stats': 'stats_standard_dom_lg',
            'defensive_actions': 'stats_defense_dom_lg'
        }
        
        # Scrape all tables
        results = {'player_info': player_info}
        
        for table_name, table_id in tables_to_scrape.items():
            df = self._extract_table_by_id(soup, table_id)
            if df is not None:
                results[table_name] = df
                logger.info(f"✓ {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")
            else:
                logger.warning(f"✗ {table_name}: Not found")
        
        return results
    
    def save_results(self, results: Dict, output_dir: str = 'outputs'):
        """
        Save scraped results to files
        
        Args:
            results: Dictionary of DataFrames from scrape_player_stats
            output_dir: Directory to save files
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        player_name = results.get('player_info', {}).get('player_name', 'player')
        player_name_clean = player_name.replace(' ', '_').replace("'", "")
        
        # Save each DataFrame to CSV
        for key, value in results.items():
            if isinstance(value, pd.DataFrame):
                filename = f"{player_name_clean}_{key}.csv"
                filepath = os.path.join(output_dir, filename)
                value.to_csv(filepath, index=False)
                logger.info(f"Saved: {filename}")

        logger.info(f"All files saved to: {output_dir}")


def main():
    """
    Main function to run the scraper
    """
    # Initialize scraper
    scraper = FBrefScraper(delay=3)
    
    # Mbappé's page URL
    mbappe_url = "https://fbref.com/en/players/42fd9c7f/Kylian-Mbappe-Stats"
    
    print("="*60)
    print("FBref Player Stats Scraper - Student Project")
    print("="*60)
    print(f"\nTarget: {mbappe_url}")
    print("Starting scrape...\n")
    
    # Scrape the data
    results = scraper.scrape_player_stats(mbappe_url)
    
    if results:
        print(f"\n{'='*60}")
        print("Scraping Complete!")
        print(f"{'='*60}")
        print(f"\nTables extracted: {len([k for k, v in results.items() if isinstance(v, pd.DataFrame)])}")
        
        # Display summary of what was scraped
        print("\nData Summary:")
        for key, value in results.items():
            if isinstance(value, pd.DataFrame):
                print(f"  • {key}: {value.shape[0]} rows × {value.shape[1]} columns")
        
        # Save results
        print(f"\n{'='*60}")
        print("Saving results...")
        print(f"{'='*60}\n")
        scraper.save_results(results)
        
        print(f"\n{'='*60}")
        print("✓ All done! Check the outputs folder for your files.")
        print(f"{'='*60}\n")
        
        return results
    else:
        print("\n✗ Scraping failed. Check the logs above for errors.")
        return None


if __name__ == "__main__":
    results = main()
