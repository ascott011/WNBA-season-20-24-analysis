import os
import json
import csv

# Directory containing the JSON files
SEASON_DATA_DIR = 'season-data'
OUTPUT_CSV = 'data/wnba_teams_seasons.csv'

# Get all JSON files in the season-data directory
json_files = [f for f in os.listdir(SEASON_DATA_DIR) if f.endswith('.json')]

# Collect all possible keys from all files for own_record['total']
all_total_keys = set()
for json_file in json_files:
    with open(os.path.join(SEASON_DATA_DIR, json_file), 'r') as f:
        data = json.load(f)
        total = data.get('own_record', {}).get('total', {})
        all_total_keys.update(total.keys())
all_total_keys = sorted(all_total_keys)

# Define the columns for the CSV
header = [
    'id', 'name', 'market', 'season'
] + all_total_keys

rows = []

for json_file in json_files:
    with open(os.path.join(SEASON_DATA_DIR, json_file), 'r') as f:
        data = json.load(f)
        row = {
            'id': data.get('id'),
            'name': data.get('name'),
            'market': data.get('market'),
            'season': data.get('season', {}).get('year'),
        }
        own_record_total = data.get('own_record', {}).get('total', {})
        for key in all_total_keys:
            row[key] = own_record_total.get(key)
        rows.append(row)

# Ensure output directory exists
os.makedirs('data', exist_ok=True)

# Write to CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Exported {len(rows)} rows to {OUTPUT_CSV}") 