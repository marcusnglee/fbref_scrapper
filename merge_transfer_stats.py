"""
Merge transfer data with player statistics from the season BEFORE the transfer
"""

import pandas as pd
import os
import glob
from typing import Optional

def parse_transfer_season(season_str: str) -> str:
    """
    Convert transfer season format to FBref season format
    '10/11' → '2009-2010' (previous season)

    Args:
        season_str: Season string like '10/11'

    Returns:
        Previous season in FBref format like '2009-2010'
    """
    # Parse the transfer season
    parts = season_str.split('/')
    start_year = int('20' + parts[0])  # '10' → 2010

    # Get PREVIOUS season
    prev_start = start_year - 1
    prev_end = start_year

    return f"{prev_start}-{prev_end}"


def get_player_stats(player_name: str, target_season: str, stats_type: str = 'standard_stats') -> Optional[pd.Series]:
    """
    Get combined stats for a player in a specific season

    Args:
        player_name: Player name
        target_season: Season in FBref format (e.g., '2009-2010')
        stats_type: Type of stats ('standard_stats' or 'defensive_actions')

    Returns:
        Combined stats for that season as a Series, or None if not found
    """
    # Clean player name for file matching
    clean_name = player_name.replace(' ', '_').replace("'", "")

    # Find the stats file
    pattern = f"outputs/{clean_name}_{stats_type}.csv"
    files = glob.glob(pattern)

    if not files:
        return None

    try:
        # Read the stats file
        df = pd.read_csv(files[0])

        # Filter for target season
        season_stats = df[df['Season'] == target_season]

        if season_stats.empty:
            return None

        # If multiple rows (multiple clubs), combine stats
        if len(season_stats) > 1:
            # Sum numeric columns, keep first value for non-numeric
            combined = season_stats.select_dtypes(include='number').sum()

            # Add back non-numeric columns (take first)
            for col in season_stats.select_dtypes(exclude='number').columns:
                if col not in ['Squad', 'Comp']:  # Don't include club/comp since we're combining
                    combined[col] = season_stats[col].iloc[0]

            combined['Squad'] = 'Combined'
            combined['Season'] = target_season

            return combined
        else:
            return season_stats.iloc[0]

    except Exception as e:
        print(f"Error reading stats for {player_name}: {e}")
        return None


def merge_transfers_with_stats(transfers_csv: str = 'transfers_1.csv',
                                output_csv: str = 'merged_transfer_stats.csv'):
    """
    Merge transfer data with player statistics from previous season

    Args:
        transfers_csv: Path to transfers CSV
        output_csv: Path for output merged CSV
    """
    print("="*60)
    print("Merging Transfer Data with Player Statistics")
    print("="*60)
    print()

    # Read transfers
    print(f"Reading transfers from: {transfers_csv}")
    transfers = pd.read_csv(transfers_csv)
    print(f"Found {len(transfers)} transfers")
    print()

    # Prepare results
    results = []
    not_found = []

    print("Matching transfers to previous season stats...")
    print()

    for idx, transfer in transfers.iterrows():
        player_name = transfer['Player']
        transfer_season = transfer['Season']

        # Get previous season in FBref format
        prev_season = parse_transfer_season(transfer_season)

        # Get stats
        standard_stats = get_player_stats(player_name, prev_season, 'standard_stats')
        defensive_stats = get_player_stats(player_name, prev_season, 'defensive_actions')

        if standard_stats is not None:
            # Combine transfer data with stats
            merged_row = transfer.copy()

            # Add stats columns with prefix
            for col, val in standard_stats.items():
                if col not in ['Season']:  # Don't duplicate season
                    merged_row[f'Stats_{col}'] = val

            # Add defensive stats if available
            if defensive_stats is not None:
                for col, val in defensive_stats.items():
                    if col not in ['Season', 'Squad', 'Comp']:
                        merged_row[f'Def_{col}'] = val

            merged_row['Stats_Season'] = prev_season
            results.append(merged_row)

            if (idx + 1) % 100 == 0:
                print(f"  Processed {idx + 1}/{len(transfers)} transfers...")
        else:
            not_found.append({
                'Player': player_name,
                'Transfer_Season': transfer_season,
                'Looking_For': prev_season
            })

    print(f"\nCompleted processing {len(transfers)} transfers")
    print()

    # Create merged dataframe
    if results:
        merged_df = pd.DataFrame(results)

        # Save to CSV
        merged_df.to_csv(output_csv, index=False)
        print(f"✓ Saved {len(results)} merged records to: {output_csv}")
        print(f"  Columns: {len(merged_df.columns)}")
        print()

        # Show sample stats included
        stats_cols = [col for col in merged_df.columns if col.startswith('Stats_')]
        print(f"Stats columns included: {len(stats_cols)}")
        print(f"Sample: {', '.join(stats_cols[:10])}...")
        print()

    # Save not found list
    if not_found:
        not_found_df = pd.DataFrame(not_found)
        not_found_file = 'merge_not_found.csv'
        not_found_df.to_csv(not_found_file, index=False)
        print(f"⚠ {len(not_found)} players not found → {not_found_file}")
        print()

    # Summary
    print("="*60)
    print("MERGE SUMMARY")
    print("="*60)
    print(f"Total transfers:        {len(transfers)}")
    print(f"Successfully matched:   {len(results)} ({len(results)/len(transfers)*100:.1f}%)")
    print(f"Not found:              {len(not_found)} ({len(not_found)/len(transfers)*100:.1f}%)")
    print("="*60)
    print()
    print(f"Output file: {output_csv}")
    print()
    print("Column structure:")
    print("  - Original transfer data (Player, Fee, Season, etc.)")
    print(f"  - Stats_* columns: Previous season stats ({len([c for c in merged_df.columns if c.startswith('Stats_')])} columns)")
    print(f"  - Def_* columns: Defensive stats ({len([c for c in merged_df.columns if c.startswith('Def_')])} columns)")
    print()


def main():
    """Main function"""

    # Check if outputs directory exists
    if not os.path.exists('outputs'):
        print("Error: outputs/ directory not found!")
        print("Run scraping first to generate player stats.")
        return

    # Check if any CSV files exist
    csv_files = glob.glob('outputs/*_standard_stats.csv')
    if not csv_files:
        print("Error: No player stat files found in outputs/!")
        print("Run scraping first to generate player stats.")
        return

    print(f"Found {len(csv_files)} player stat files in outputs/")
    print()

    # Run merge
    merge_transfers_with_stats()

    print("Done! You can now analyze the merged data:")
    print("  import pandas as pd")
    print("  df = pd.read_csv('merged_transfer_stats.csv')")
    print()


if __name__ == "__main__":
    main()
