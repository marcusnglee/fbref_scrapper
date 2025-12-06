"""
Quick test script to scrape 2-3 players
"""
from scrape_multiple_players import scrape_multiple_players

# Test with just 2 players to verify it works
test_players = {
    "Vinicius Jr": "https://fbref.com/en/players/5ade27f0/Vinicius-Junior-Stats",
    "Jude Bellingham": "https://fbref.com/en/players/a381b824/Jude-Bellingham-Stats",
}

print("Testing the scraper with 2 players...")
results = scrape_multiple_players(test_players, delay=4)

print(f"\n{'='*60}")
print("Test Complete!")
print(f"{'='*60}")
