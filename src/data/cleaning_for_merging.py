import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz


def normalize_names(df):
    def remove_on_loan_from(s):
        if "(" in s:
            return s[: s.find("(")].strip()
        else:
            return s     
    df["Name"] = df["Name"].apply(remove_on_loan_from)
    df["Name"] = df["Name"].apply(unidecode)
    df["Name"] = df["Name"].str.replace("-", " ")
    df["Name"] = df["Name"].str.lower()
    return df


def match_players_with_different_names(df1, df2):

    diff_df1 = df1[~df1["Name"].isin(df2["Name"])]
    diff_sal = df2[~df2["Name"].isin(df1["Name"])]

    for idx, player_df1 in diff_df1.iterrows():
        for _, player_sal in diff_sal.iterrows():
            a = player_df1["Name"]
            b = player_sal["Name"]
            same_names = set(a.split()).issubset(set(b.split())) or set(b.split()).issubset(
                set(a.split())
            )
            nicknames = (player_df1["Name"] in player_sal["Name"]) or (
                player_sal["Name"] in player_df1["Name"]
            )
            same_team = player_df1["Team"] == player_sal["Team"]
            ratio = fuzz.ratio(player_df1["Name"], player_sal["Name"])
            if (same_names or nicknames or ratio > 70) and same_team:
                df1.loc[idx, "Name"] = player_sal["Name"]

    return df1

def drop_distinct_rows(df1, df2):
    drop_indeces = df1[~df1["Name"].isin(df2["Name"])].index
    df1 = df1.drop(drop_indeces).reset_index(drop=True)
    return df1