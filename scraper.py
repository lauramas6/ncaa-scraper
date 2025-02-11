# NCAA D1 Women's Soccer Score Scraper
# Author: Laura Mas and Sean Steele

import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from fpdf import FPDF
import pytz


# NCAA Women's Soccer Scores URL
NCAA_URL = "https://www.ncaa.com/scoreboard/soccer-women/d1"

# Fetch data and returns scores
def fetch_scores():
    response = requests.get(NCAA_URL)
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    games = []

    # Selectors based on NCAA's website attributes
    for game in soup.find_all("div", class_="gamePod"):
        print("Found a game block")  # Debugging line
        teams = game.find_all("span", class_="gamePod-game-team-name")
        scores = game.find_all("span", class_="gamePod-game-team-score")

        if len(teams) == 2 and len(scores) == 2:
            games.append({
                "team_1": teams[0].text.strip(),
                "score_1": scores[0].text.strip(),
                "team_2": teams[1].text.strip(),
                "score_2": scores[1].text.strip(),
                "date": datetime.now().strftime("%Y-%m-%d")
            })

    print(f"Found {len(games)} games")  # Helper line

    return games

# JSON file generator
def save_data(data):
    if not os.path.exists("data"):
        # print("Creating data directory")  # Helper line
        os.makedirs("data")

    pacific_tz = pytz.timezone("America/Los_Angeles")
    pacific_time = datetime.now(pacific_tz).strftime('%Y-%m-%d')

    json_filename = f"data/scores_{pacific_time}.json"
    # print(f"Saving data to {json_filename}")  # Helper line
    with open(json_filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved {len(data)} games to {json_filename}")

    # Save data as PDF
    pdf_filename = f"data/scores_{pacific_time}.pdf"
    create_pdf(data, pdf_filename)

# PDF file generator
def create_pdf(data, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Properties
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="NCAA D1 Women's Soccer Scores", ln=True, align='C')

    # Add scores
    for game in data:
        game_info = f"{game['team_1']} {game['score_1']} - {game['team_2']} {game['score_2']}"
        pdf.ln(10)
        pdf.cell(200, 10, txt=game_info, ln=True)

    # Save PDF
    pdf.output(filename)
    print(f"Saved PDF report to {filename}")

if __name__ == "__main__":
    scores = fetch_scores()
    if scores:
        save_data(scores)

