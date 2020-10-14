# This script allow to scrape www.spotrac.com and extract
# EPL football players salaries.


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

url = "https://www.spotrac.com/epl/rankings/2018/"
name = "salaries_2018_2019"

os.chdir("inputs")
data = {"ajax": "true", "mobile": "false"}
soup = BeautifulSoup(requests.post(url, data=data).content, "html.parser")
df = pd.DataFrame(columns=["Name", "Position", "Team", "Salary"])

row = []
for h3 in soup.select("h3"):
    row.append(h3.text.strip())
    row.append(h3.find_next(class_="rank-position").text.strip())
    row.append(h3.find_next(class_="center").text.strip())
    row.append(h3.find_next(class_="rank-value").text.strip())
    df.loc[len(df)] = row
    row = []

df.to_csv(name + ".csv", index=False)
