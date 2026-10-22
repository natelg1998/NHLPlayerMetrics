import numpy as np  
import pandas as pd 
import requests 

FRANCHISE_API_URL = "https://api.nhle.com/stats/rest/en/franchise"
def extract_franchise_data(url = FRANCHISE_API_URL):
    resp = requests.get(FRANCHISE_API_URL).json()
    franchise_df = pd.DataFrame(resp['data'])
    franchise_df.rename(columns={'id': 'Franchise ID', 'fullName': 'Name', 'teamCommonName': "Team Shortname", 
                                 'teamPlaceName': "Location"}, inplace=True)
    return franchise_df



if __name__ == '__main__':
    df = extract_franchise_data()
    print(df.sort_values(by='Franchise ID'))
    
    
    