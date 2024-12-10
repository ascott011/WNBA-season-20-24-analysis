import requests
import json
import time
import os
from dotenv import load_dotenv

#import env variables
load_dotenv()

#get api key from env file
API_KEY = os.getenv('SPORTRADAR_API_KEY')


seasons = ['2020', '2021', '2022', '2023', '2024']

#creates a folder for season data
os.makedirs('season-data', exist_ok=True)

# Load team IDs from json file with ids
with open('wnba-team-ids.json', 'r') as file:
    team_objects = json.load(file)

# Extract just the IDs from the team info
team_ids = [team['id'] for team in team_objects]

for team_id in team_ids:
    for season in seasons:
        # Check if file already exists
        file_name = f"season-data/wnba_season_{season}_team_{team_id}_data.json"
        if os.path.exists(file_name):
            print(f"File {file_name} already exists")
            continue

        url = f"http://api.sportradar.com/wnba/trial/v8/en/seasons/{season}/REG/teams/{team_id}/statistics.json?api_key={API_KEY}"
       
        print(f"Trying URL: {url}")
        try:
            response = requests.get(url)
            print(f"Response status: {response.status_code}")
           
            if response.status_code == 200:
                data = response.json()
               
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=2)

                print(f"Data for team {team_id} in {season} season saved")
               
                # Wait 2.2 seconds between requests (trial accounts typically allow 1 request per second)
                time.sleep(2.2)
            else:
                print(f"Failed to fetch data for team {team_id} in season {season}")

        except Exception as e:
            print(f"An error occurred while fetching data for team {team_id} in season {season}: {e}")