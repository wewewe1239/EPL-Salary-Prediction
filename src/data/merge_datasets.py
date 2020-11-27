import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import os

from data.cleaning_for_merging import (
    normalize_names,
    match_players_with_different_names,
    drop_distinct_rows,
)


def merge_stats_and_salaries():
    player_stats = "data/raw/players_stats_2018_2019.csv"
    salaries = "data/raw/salaries_2018_2019.csv"

    stats = pd.read_csv(player_stats)
    salaries = pd.read_csv(salaries)

    stats = normalize_names(stats)
    salaries = normalize_names(salaries)

    stats = match_players_with_different_names(stats, salaries)

    stats = drop_distinct_rows(stats, salaries)

    df = pd.merge(stats, salaries, how="inner", on=["Name", "Team"])

    df["Pos"] = df["Position"]
    columns_to_drop = ["Team", "Name", "Nat", "Position"]
    df = df.drop(columns_to_drop, axis=1)

    return df


df = merge_stats_and_salaries()

df.to_csv("data/interim/stats_&_salaries_2018_2019.csv", index=False)
