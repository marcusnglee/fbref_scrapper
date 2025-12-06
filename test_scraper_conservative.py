"""
Conservative test with longer delays
"""
from scrape_multiple_players import scrape_multiple_players

# Test with just 1 new player (we already have Mbappé)
test_players = {
    "Erling Haaland": "https://fbref.com/en/players/1f44ac21/Erling-Haaland-Stats",
}

print("Testing with 1 player and conservative delays...")
results = scrape_multiple_players(test_players, delay=8)

print(f"\n{'='*60}")
print("Test Complete!")
print(f"{'='*60}")
