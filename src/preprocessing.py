import pandas as pd
from unidecode import unidecode


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