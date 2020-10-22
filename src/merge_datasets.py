import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import os

from preprocessing import normalize_names, match_players_with_different_names

def merge_stats_and_salaries():
    player_stats = "data/raw/players_stats_2018_2019.csv"
    salaries = "data/raw/salaries_2018_2019.csv"

    stats = pd.read_csv(player_stats)
    salaries = pd.read_csv(salaries)

    dfs = [stats, salaries]
    
    for df in dfs:
        df = normalize_names(df)


    stats = match_players_with_different_names(stats, salaries)



    drop_index = stats[~stats["Name"].isin(salaries["Name"])].index
    stats = stats.drop(drop_index).reset_index(drop=True)


    df = pd.merge(stats, salaries, how="inner", on=["Name", "Team"])

    df["Pos"] = df["Position"]
    columns_to_drop = ["Team", "Name", "Nat", "Position"]
    df = df.drop(columns_to_drop, axis=1)

    return df

df = merge_stats_and_salaries()





# os.chdir("data/interim")
# df.to_csv("stats_&_salaries_2018_2019wewe.csv", index=False)

print(os.getcwd())

