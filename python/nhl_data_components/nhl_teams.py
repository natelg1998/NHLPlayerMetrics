import numpy as np  
import pandas as pd 
import requests 

TEAMS_API_URL = "https://api.nhle.com/stats/rest/en/team"
def extract_teams_data(url = TEAMS_API_URL):
    resp = requests.get(TEAMS_API_URL).json()
    teams_df = pd.DataFrame(resp['data'])
    teams_df.rename(columns={'id': 'Team ID', 'franchiseId': 'Franchise ID', 'fullName': 'Team Name', "triCode":"Team Code"}, inplace=True)
    teams_df.drop(['leagueId', 'rawTricode'], axis = 1, inplace=True)
    return teams_df



if __name__ == '__main__':
    df = extract_teams_data()
    print(df[df['Team ID'] == 9])
    
    
    