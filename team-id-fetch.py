import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('SPORTRADAR_API_KEY')

def get_team_ids():
    if not API_KEY:
        raise ValueError("API_KEY not found in env file")
    
    url = f"http://api.sportradar.com/wnba/trial/v8/en/league/teams.json?api_key={API_KEY}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            team_ids = [{"id": team["id"],"market": team["market"], "name": team["name"]} for team in data.get("teams", [])]

            file_name = "wnba-team-ids.json"

            with open(file_name, 'w') as file:
                json.dump(team_ids, file, indent=2)

            print("WNBA Team IDs sucessfully saved")
       
        else:
            print("Failed to fetch team IDs")

    except Exception as e:
        print("An error occured while fetching data reason {e}")

get_team_ids()