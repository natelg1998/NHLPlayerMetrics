
import numpy as np  
import pandas as pd 
import requests 
from pprint import pprint
import pytz

NHL_SCHEDULE_URL = "https://api.nhle.com/stats/rest/en/game"

query_params = {
    "start":0,
    "cayenneExp": "season >= 20202021 and gameType in (2,3)"
}

def get_game_info(season_start, season_end=None, include_preseason=False):
    if season_end and include_preseason:
        query_params = {
            "start":0,
            "cayenneExp": f"season >= {season_start} and season <= {season_end}"
            }
    elif season_end:
        query_params = {
            "start":0,
            "cayenneExp": f"season >= {season_start} and season <= {season_end} and gameType in (2,3)"
                } 
    elif include_preseason:
            query_params = {
                "start":0,
                "cayenneExp": f"season >= {season_start}"
                    } 
    else:
        query_params = {
            "start":0,
            "cayenneExp": f"season >={season_start} and gameType in (2,3)"
            }
        
    resp = requests.get(NHL_SCHEDULE_URL, params=query_params).json()
    df = pd.DataFrame(resp['data'])
    df = df.rename(columns = {
        "id": "Game ID",
        "easternStartTime": "Gametime EPT",
        "gameDate": "Game Date",
        "gameNumber": "Game Number",
        "gameScheduleStateId": "Game Schedule State ID",
        "gameStateId": "Game State ID",
        "gameType": "Game Type",
        "homeScore": "Home Score",
        "homeTeamId": "Home Team ID",
        "visitingScore": "Away Score",
        "visitingTeamId": "Away Team ID",
        "season": "Season ID"
    })
    df.drop(["period"], axis=1, inplace = True)
    df = df.astype({
        "Game ID": pd.Int64Dtype(),
        "Gametime EPT": "datetime64[us]",
        "Game Date": "datetime64[us]",
        "Game Number": pd.Int64Dtype(),
        "Game Schedule State ID": pd.Int64Dtype(),
        "Game State ID": pd.Int64Dtype(),
        "Game Type": pd.Int64Dtype(),
        "Home Score": pd.Int64Dtype(),
        "Home Team ID": pd.Int64Dtype(),
        "Away Score": pd.Int64Dtype(),
        "Away Team ID": pd.Int64Dtype(),
        "Season ID":pd.Int64Dtype()
        
    })
    return df


if __name__ == "__main__":
    games = get_game_info(season_start=20242025, season_end=20242025)
    print(games.head())