import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import os

from preprocessing import normalize_names

def merge_stats_and_salaries():
    player_stats = "data/raw/players_stats_2018_2019.csv"
    salaries = "data/raw/salaries_2018_2019.csv"

    stats = pd.read_csv(player_stats)
    salaries = pd.read_csv(salaries)

    dfs = [stats, salaries]
    
    for df in dfs:
        df = normalize_names(df)


    # diff_stats = stats[~stats["Name"].isin(salaries["Name"])]
    # diff_sal = salaries[~salaries["Name"].isin(stats["Name"])]

    # for idx, player_stats in diff_stats.iterrows():
    #     for _, player_sal in diff_sal.iterrows():
    #         a = player_stats["Name"]
    #         b = player_sal["Name"]
    #         same_names = set(a.split()).issubset(set(b.split())) or set(b.split()).issubset(
    #             set(a.split())
    #         )
    #         nicknames = (player_stats["Name"] in player_sal["Name"]) or (
    #             player_sal["Name"] in player_stats["Name"]
    #         )
    #         same_team = player_stats["Team"] == player_sal["Team"]
    #         ratio = fuzz.ratio(player_stats["Name"], player_sal["Name"])
    #         if (same_names or nicknames or ratio > 70) and same_team:
    #             stats.loc[idx, "Name"] = player_sal["Name"]


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

