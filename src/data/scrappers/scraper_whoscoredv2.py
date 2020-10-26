# This script allow to scrape www.whoscored.com and extract
# players statistics during a season.
# The Web Scraper is partly inspired by a solution available on this
# link : https://github.com/cboutaud/whoscraped. The structure of
# the website's pages has changed since then, we had to ajust some
# features and increase the robustness by adding an exception management 
# mechanism for when pages are not proprely charged.
#########################################################################

# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os

# Base URL
baseURL = "https://www.whoscored.com/Teams/"

# EPL Teams
eplTeams = [
    "167",  # MCFC / Manchester City
    "32",  # MUFC / Manchester United
    "30",  # THFC / Tottenham Hotspur
    "26",  # LFC / Liverpool FC
    "15",  # CFC / Chelsea FC
    "13",  # AFC / Arsenal FC
    "184",  # BFC / Burnley FC
    "31",  # EFC / Everton FC
    "14",  # LC / Leicester City
    "23",  # NUFC / Newcastle United
    "162",  # CP / Crystal Palace
    "183",  # BOU / AFC Bournemouth
    "29",  # WHUFC / West Ham United
    "27",  # WAT / Watford FC
    "211",  # BHA / Brighton & Hove Albion
    "166",  # HUD / Huddersfield Town
    "18",  # SFC / Southampton FC
    "161",  # WWFC / Wolverhampton Wanderers
    "188",  # CCFC / Cardiff City
    "170",  # FFC / Fulham FC
]

# Mapping Team ID -> Team Name
teams_ID_to_name = {
    "167": "MCFC",
    "32": "MUFC",
    "30": "THFC",
    "26": "LFC",
    "15": "CFC",
    "13": "AFC",
    "184": "BFC",
    "31": "EFC",
    "14": "LC",
    "23": "NUFC",
    "162": "CP",
    "183": "BOU",
    "29": "WHUFC",
    "27": "WAT",
    "211": "BHA",
    "166": "HUD",
    "18": "SFC",
    "161": "WWFC",
    "188": "CCFC",
    "170": "FFC",
}

archiveUrl = "/Archive?stageId=16368"  # season 2018/2019

os.chdir("data/raw")
outputfile = open("players_stats_2018_2019.csv", "w")
csv_writer = csv.writer(outputfile)
csv_writer.writerow(
    [
        "Name",
        "Team",
        "Nat",  # Nationality
        "Age",
        "Pos",  # Position in field
        "Height",
        "Weight",
        "Apps(Subs)",  # Appearances
        "Mins",  # Mins played
        "Goals",  # Total goals
        "Assists",  # Total assists
        "Yel",  # Yellow cards
        "Red",  # Red cards
        "SpG",  # Shots per game
        "PS%",  # Pass success percentage
        "AerWon",  # Aerial duels won per game
        "MoM",  # Man of the match
        "Tackles",  # Tackles per game
        "Inter",  # Interceptions per game
        "Fouls",  # Fouls per game
        "OffW",  # Offsides won per game
        "Clear",  # Clearances per game
        "DrbPast",  # Dribbled past per game
        "Blocks",  # Outfielder block per game
        "OwnG",  # Own goals
        "KeyP",  # Key passes per game
        "Drb",  # Dribbles per game
        "Fouled",  # Fouled per game
        "Off",  # Offsides per game
        "Disp",  # Dspossessed per game
        "UnsT",  # Bad control per game
        "AvgP",  # Passes per game
        "Crosses",  # Crosses per game
        "LongB",  # Long balls per game
        "ThrB",  # Through balls per game
        "Rat",  # Rating
    ]
)
for team in eplTeams:
    print("Currently getting {}'s players data ...".format(teams_ID_to_name[team]))

    ALLTHEDAMNPLAYERS = {}

    # URL
    finalURL = baseURL + team + archiveUrl

    # Connect webdriver
    browser = webdriver.Firefox()
    browser.set_window_size(1920, 1080)
    browser.get(finalURL)
    time.sleep(3)

    # Different tables
    tableNames = tableNames = ["summary", "defensive", "offensive", "passing"]

    # Get all tables
    tables = []

    for tableName in tableNames:
        while True:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "a[href*='#team-squad-archive-stats-" + tableName + "']",
                    )
                )
            )
            time.sleep(10)
            browser.execute_script("arguments[0].click();", element)
            time.sleep(10)

            # Get content
            content = browser.page_source
            soup = BeautifulSoup("".join(content), "lxml")
            table = soup.find("div", {"id": "statistics-table-" + tableName}).find(
                "tbody", {"id": "player-table-statistics-body"}
            )
            try:
                test_NoneType = table.findAll("tr")[0].findAll("td")
                break
            except AttributeError:
                print(
                    "An error with the page has occured, refreshing and trying again ..."
                )
                browser.refresh()
                time.sleep(10)
                continue
        tables.append(table)
        print("\t" + tableName + "\t" + u"\u2713")

    browser.quit()

    j = 0

    for table in tables:

        # Get players
        players = table.findAll("tr")

        # Get stats
        for i in range(len(players)):
            stats = players[i].findAll("td")

            if j == 0:
                index = stats[0].get_text().split()[0][0]
                nation = stats[1].find("span").get("class")[2].rsplit("-", 1)[1]
                name = stats[1].findChildren()[0].get_text().strip()
                players_team = teams_ID_to_name[team]
                age = stats[1].findChildren()[2].get_text().strip()
                pos = stats[1].findChildren()[3].get_text().split(",", 1)[1].strip()
                cm = stats[2].get_text().strip()
                kg = stats[3].get_text().strip()
                apps = stats[4].get_text().strip()
                mins = stats[5].get_text().strip()
                goals = stats[6].get_text().strip()
                assists = stats[7].get_text().strip()
                yellow = stats[8].get_text().strip()
                red = stats[9].get_text().strip()
                SpG = stats[10].get_text().strip()
                PassPer = stats[11].get_text().strip()
                AerialsWon = stats[12].get_text().strip()
                MotM = stats[13].get_text().strip()

                ALLTHEDAMNPLAYERS[name] = []
                ALLTHEDAMNPLAYERS[name].append(players_team)
                ALLTHEDAMNPLAYERS[name].append(nation)
                ALLTHEDAMNPLAYERS[name].append(age)
                ALLTHEDAMNPLAYERS[name].append(pos)
                ALLTHEDAMNPLAYERS[name].append(cm)
                ALLTHEDAMNPLAYERS[name].append(kg)
                ALLTHEDAMNPLAYERS[name].append(apps)
                ALLTHEDAMNPLAYERS[name].append(mins)
                ALLTHEDAMNPLAYERS[name].append(goals)
                ALLTHEDAMNPLAYERS[name].append(assists)
                ALLTHEDAMNPLAYERS[name].append(yellow)
                ALLTHEDAMNPLAYERS[name].append(red)
                ALLTHEDAMNPLAYERS[name].append(SpG)
                ALLTHEDAMNPLAYERS[name].append(PassPer)
                ALLTHEDAMNPLAYERS[name].append(AerialsWon)
                ALLTHEDAMNPLAYERS[name].append(MotM)

            if j == 1:
                name = stats[1].findChildren()[0].get_text().strip()
                tackles = stats[6].get_text().strip()
                inter = stats[7].get_text().strip()
                fouls = stats[8].get_text().strip()
                offW = stats[9].get_text().strip()
                clear = stats[10].get_text().strip()
                drbP = stats[11].get_text().strip()
                blocks = stats[12].get_text().strip()
                ownG = stats[13].get_text().strip()

                ALLTHEDAMNPLAYERS[name].append(tackles)
                ALLTHEDAMNPLAYERS[name].append(inter)
                ALLTHEDAMNPLAYERS[name].append(fouls)
                ALLTHEDAMNPLAYERS[name].append(offW)
                ALLTHEDAMNPLAYERS[name].append(clear)
                ALLTHEDAMNPLAYERS[name].append(drbP)
                ALLTHEDAMNPLAYERS[name].append(blocks)
                ALLTHEDAMNPLAYERS[name].append(ownG)

            if j == 2:
                name = stats[1].findChildren()[0].get_text().strip()
                KP = stats[9].get_text().strip()
                drb = stats[10].get_text().strip()
                fouled = stats[11].get_text().strip()
                cOff = stats[12].get_text().strip()
                disp = stats[13].get_text().strip()
                unsT = stats[14].get_text().strip()

                ALLTHEDAMNPLAYERS[name].append(KP)
                ALLTHEDAMNPLAYERS[name].append(drb)
                ALLTHEDAMNPLAYERS[name].append(fouled)
                ALLTHEDAMNPLAYERS[name].append(cOff)
                ALLTHEDAMNPLAYERS[name].append(disp)
                ALLTHEDAMNPLAYERS[name].append(unsT)

            if j == 3:
                name = stats[1].findChildren()[0].get_text().strip()
                avgP = stats[8].get_text().strip()
                crosses = stats[10].get_text().strip()
                longB = stats[11].get_text().strip()
                thrB = stats[12].get_text().strip()
                rat = stats[13].get_text().strip()

                ALLTHEDAMNPLAYERS[name].append(avgP)
                ALLTHEDAMNPLAYERS[name].append(crosses)
                ALLTHEDAMNPLAYERS[name].append(longB)
                ALLTHEDAMNPLAYERS[name].append(thrB)
                ALLTHEDAMNPLAYERS[name].append(rat)

        j += 1

    for indiv in ALLTHEDAMNPLAYERS:
        csv_writer.writerow(
            [
                indiv,
                ALLTHEDAMNPLAYERS[indiv][0],
                ALLTHEDAMNPLAYERS[indiv][1],
                ALLTHEDAMNPLAYERS[indiv][2],
                ALLTHEDAMNPLAYERS[indiv][3],
                ALLTHEDAMNPLAYERS[indiv][4],
                ALLTHEDAMNPLAYERS[indiv][5],
                ALLTHEDAMNPLAYERS[indiv][6],
                ALLTHEDAMNPLAYERS[indiv][7],
                ALLTHEDAMNPLAYERS[indiv][8],
                ALLTHEDAMNPLAYERS[indiv][9],
                ALLTHEDAMNPLAYERS[indiv][10],
                ALLTHEDAMNPLAYERS[indiv][11],
                ALLTHEDAMNPLAYERS[indiv][12],
                ALLTHEDAMNPLAYERS[indiv][13],
                ALLTHEDAMNPLAYERS[indiv][14],
                ALLTHEDAMNPLAYERS[indiv][15],
                ALLTHEDAMNPLAYERS[indiv][16],
                ALLTHEDAMNPLAYERS[indiv][17],
                ALLTHEDAMNPLAYERS[indiv][18],
                ALLTHEDAMNPLAYERS[indiv][19],
                ALLTHEDAMNPLAYERS[indiv][20],
                ALLTHEDAMNPLAYERS[indiv][21],
                ALLTHEDAMNPLAYERS[indiv][22],
                ALLTHEDAMNPLAYERS[indiv][23],
                ALLTHEDAMNPLAYERS[indiv][24],
                ALLTHEDAMNPLAYERS[indiv][25],
                ALLTHEDAMNPLAYERS[indiv][26],
                ALLTHEDAMNPLAYERS[indiv][27],
                ALLTHEDAMNPLAYERS[indiv][28],
                ALLTHEDAMNPLAYERS[indiv][29],
                ALLTHEDAMNPLAYERS[indiv][30],
                ALLTHEDAMNPLAYERS[indiv][31],
                ALLTHEDAMNPLAYERS[indiv][32],
                ALLTHEDAMNPLAYERS[indiv][33],
                ALLTHEDAMNPLAYERS[indiv][34],
            ]
        )
