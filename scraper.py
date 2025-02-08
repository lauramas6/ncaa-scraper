import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

# NCAA Women's Soccer Scores URL (update with the correct URL)
NCAA_URL = "https://www.ncaa.com/scoreboard/soccer-women/d1"

def fetch_scores():
    response = requests.get(NCAA_URL)
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    games = []

    # Modify selectors based on NCAA's website structure
    for game in soup.find_all("div", class_="game-block"):
        teams = game.find_all("span", class_="team-name")
        scores = game.find_all("span", class_="team-score")

        if len(teams) == 2 and len(scores) == 2:
            games.append({
                "team_1": teams[0].text.strip(),
                "score_1": scores[0].text.strip(),
                "team_2": teams[1].text.strip(),
                "score_2": scores[1].text.strip(),
                "date": datetime.now().strftime("%Y-%m-%d")
            })

    return games

def save_data(data):
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/scores_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved {len(data)} games to {filename}")

if __name__ == "__main__":
    scores = fetch_scores()
    if scores:
        save_data(scores)

