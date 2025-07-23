import os
import json
import csv

# Directory containing the JSON files
SEASON_DATA_DIR = 'season-data'
OUTPUT_CSV = 'data/wnba_teams_seasons.csv'

# Ensure output directory exists
# os.makedirs('data', exist_ok=True)

# Get all JSON files in the season-data directory
json_files = [f for f in os.listdir(SEASON_DATA_DIR) if f.endswith('.json')]

# Use the first file to determine the columns under own_record->total
sample_file = os.path.join(SEASON_DATA_DIR, json_files[0])
with open(sample_file, 'r') as f:
    sample_data = json.load(f)
    own_record_total_keys = list(sample_data['own_record']['total'].keys())

# Define the columns for the CSV
header = [
    'id', 'name', 'market', 'games_played', 'field_goals_made', 'field_goals_att', 'field_goals_pct'
] + own_record_total_keys

# Remove duplicates if any of the first 4 are also in own_record_total_keys
header = list(dict.fromkeys(header))

rows = []

for json_file in json_files:
    with open(os.path.join(SEASON_DATA_DIR, json_file), 'r') as f:
        data = json.load(f)
        row = {
            'id': data.get('id'),
            'name': data.get('name'),
            'market': data.get('market'),
        }
        # Add the required own_record->total fields
        own_record_total = data.get('own_record', {}).get('total', {})
        # Add the three required stats fields
        row['games_played'] = own_record_total.get('games_played')
        row['field_goals_made'] = own_record_total.get('field_goals_made')
        row['field_goals_att'] = own_record_total.get('field_goals_att')
        row['field_goals_pct'] = own_record_total.get('field_goals_pct')
        # Add all own_record->total fields
        for key in own_record_total_keys:
            row[key] = own_record_total.get(key)
        rows.append(row)

# Write to CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Exported {len(rows)} rows to {OUTPUT_CSV}") 