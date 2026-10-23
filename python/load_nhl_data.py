import mssql_python
from pandasql import sqldf
import pandas as pd
from nhl_data_components.nhl_franchises import extract_franchise_data
from nhl_db_connection import NHLDB_INSTANCE
from sqlalchemy import create_engine


sql_engine = create_engine(NHLDB_INSTANCE)
conn = sql_engine.connect()


def load_franchises():
    franchise_df = extract_franchise_data()
    cleaned_franchise_df = sqldf("""
                SELECT 
                `Franchise ID` as FranchiseID,
                 Name as FranchiseName,
                 `Team Shortname` as TeamShortname,
                 Location
                FROM franchise_df""")
    cleaned_franchise_df.to_sql(
        name = "Franchises",
        con = conn,
        schema = 'nhl',
        if_exists='delete_rows',
        index=False
    )
    

    

if __name__ == "__main__":
    load_franchises()


conn.close()


