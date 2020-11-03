# This script allow to scrape www.spotrac.com and extract
# EPL football players salaries.


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def scrap_salaries():
    df = pd.DataFrame(columns=["Name", "Position", "Team", "Salary", "Season"])
    for year in range (2015, 2020):
        url = "https://www.spotrac.com/epl/rankings/" + str(year) + "/"
        name = "salaries"
        data = {"ajax": "true", "mobile": "false"}
        soup = BeautifulSoup(requests.post(url, data=data).content, "html.parser")

        row = []
        for h3 in soup.select("h3"):
            row.append(h3.text.strip())
            row.append(h3.find_next(class_="rank-position").text.strip())
            row.append(h3.find_next(class_="center").text.strip())
            row.append(h3.find_next(class_="rank-value").text.strip())
            row.append(str(year) + "_" + str(year + 1))
            df.loc[len(df)] = row
            row = []

    df.to_csv(name + ".csv", index=False)

os.chdir("data/raw")

scrap_salaries()
