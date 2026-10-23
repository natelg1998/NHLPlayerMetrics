
import numpy as np  
import pandas as pd 
import requests 
from pprint import pprint
import pytz

SKATERS_API_URL = "https://api.nhle.com/stats/rest/en/skater/bios"
GOALIES_API_URL = "https://api.nhle.com/stats/rest/en/goalie/bios"

def get_skaters(season):
    query_parameters = {
        "limit": -1,
        "start":0,
        "sort": "playerId",
        "dir":"asc",
        "cayenneExp": f"seasonId == {season} and gameTypeId=2",
        "isAggregate":True
    }

    resp = requests.get(SKATERS_API_URL, params=query_parameters).json()
    df = pd.DataFrame(resp['data'])
    df.rename(columns = {
        "skaterFullName": "Player Name",
        "playerId": "Player ID",
        "assists":"Assists",
        "birthCity": "Birth City",
        "birthDate":"Birthdate",
        "birthCountryCode": "Birth Country",
        "birthStateProvinceCode": "Birth State/Province",
        "draftOverall":"Draft Overall",
        "draftRound": "Draft Round",
        "draftYear": "Draft Year",
        "firstSeasonForGameType":"First Season",
        "gamesPlayed": "Total Games Played",
        "goals":"Goals",
        "height":"Height",
        "positionCode":"Position",
        "nationalityCode":"Nationality",
        "points":"Points",
        "shootsCatches":"Hand",
        "weight":"Weight"
    }, inplace=True)
    df = df[["Player ID", "Player Name", "Birthdate", "Birth City", "Birth Country", "Birth State/Province", "Nationality", "Draft Overall", "Draft Round",
         "Draft Year", "First Season", "Position", "Height", "Weight", "Hand"]]
    df = df.astype({
        "Birth City": pd.StringDtype(),
        "Birth Country": pd.StringDtype(),
        "Birthdate": 'datetime64[ns]',
        "Birth State/Province": pd.StringDtype(),
        "Draft Overall": pd.Int64Dtype(),
        "Draft Round": pd.Int64Dtype(),
        "Draft Year": pd.Int64Dtype(),
        "First Season": pd.Int64Dtype(),
        "Height": pd.Int64Dtype(),
        "Nationality":pd.StringDtype(),
        "Position":pd.StringDtype(),
        "Hand":pd.StringDtype(),
        "Player Name": pd.StringDtype(),
        "Weight":pd.Int64Dtype()
        
    })
    return df

def get_goalies(season):
    query_parameters = {
        "limit": -1,
        "start":0,
        "sort": "playerId",
        "dir":"asc",
        "cayenneExp": f"seasonId == {season} and gameTypeId=2",
        "isAggregate":True
    }

    resp = requests.get(GOALIES_API_URL, params=query_parameters).json()
    df = pd.DataFrame(resp['data'])
    df.rename(columns = {
        "goalieFullName": "Player Name",
        "playerId": "Player ID",
        "birthCity": "Birth City",
        "birthDate":"Birthdate",
        "birthCountryCode": "Birth Country",
        "birthStateProvinceCode": "Birth State/Province",
        "draftOverall":"Draft Overall",
        "draftRound": "Draft Round",
        "draftYear": "Draft Year",
        "firstSeasonForGameType":"First Season",
        "goals":"Goals",
        "height":"Height",
        "nationalityCode":"Nationality",
        "shootsCatches":"Hand",
        "weight":"Weight"
    }, inplace=True)
    df["Position"] = "G"
    df = df[["Player ID", "Player Name", "Birthdate", "Birth City", "Birth Country", "Birth State/Province", "Nationality", "Draft Overall", "Draft Round",
         "Draft Year", "First Season", "Position", "Height", "Weight", "Hand"]]
    df = df.astype({
        "Birth City": pd.StringDtype(),
        "Birth Country": pd.StringDtype(),
        "Birthdate": 'datetime64[ns]',
        "Birth State/Province": pd.StringDtype(),
        "Draft Overall": pd.Int64Dtype(),
        "Draft Round": pd.Int64Dtype(),
        "Draft Year": pd.Int64Dtype(),
        "First Season": pd.Int64Dtype(),
        "Height": pd.Int64Dtype(),
        "Nationality":pd.StringDtype(),
        "Position":pd.StringDtype(),
        "Hand":pd.StringDtype(),
        "Player Name": pd.StringDtype(),
        "Weight":pd.Int64Dtype()
        
    })
    return df

if __name__ == "__main__":
    # df = get_skaters(20042005)
    # print(df.head())
    print("Skaters Check")
    all_skaters = []
    seasons_range = np.arange(19701971,20272028,10001)
    # we have to account for the NHL lockout season 2004-2005
    for season in seasons_range[seasons_range != 20042005]:
        skaters = get_skaters(season)
        all_skaters.append(skaters)
    
    all_skaters_df = pd.concat(all_skaters, ignore_index=True)
    all_skaters_df.drop_duplicates(keep='last', inplace=True)
    print(all_skaters_df.head(20).sort_values(by=['Player ID']))
    
    print("Duplicate Skaters Check")
    skater_id_counts = all_skaters_df['Player ID'].value_counts()
    print(skater_id_counts[skater_id_counts > 1])
    
    print("Goalies Check")
    all_goalies = []
    
        # we have to account for the NHL lockout season 2004-2005
    for season in seasons_range[seasons_range != 20042005]:
        goalies= get_goalies(season)
        all_goalies.append(goalies)
        
    all_goalies_df = pd.concat(all_goalies, ignore_index=True)
    all_goalies_df.drop_duplicates(keep='last', inplace=True)
    print(all_goalies_df.head(20).sort_values(by=['Player ID']))
    
    print("Duplicate Goalies Check")
    goalie_id_counts = all_goalies_df['Player ID'].value_counts()
    print(goalie_id_counts[goalie_id_counts > 1])
    
  
    

