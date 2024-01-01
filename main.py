from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def parse_team_results(team_url):
    url = f"https://football.kulichki.net/ruschamp/2024/teams/{team_url}"
    response = requests.get(url)

    results = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        championship_table = soup.find('p', string='Чемпионат России 2023/2024.').find_next('table', {'border': '1'})
        rows = championship_table.find_all('tr')

        for row in rows:
            columns = row.find_all('td')

            if columns and columns[0].text.strip().isdigit():
                tour = columns[0].text.strip()
                date = columns[1].text.strip()
                opponent = columns[2].text.strip()
                goals = columns[3].text.strip()

                result = f"{date}, {tour} тур\n{opponent}\nГолы: {goals}\n"
                results.append(result)

    else:
        results.append(f"Ошибка при запросе: {response.status_code}")

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        team_url = request.form['team_url']
        print(f"Received team_url: {team_url}")
        results = parse_team_results(team_url)
        print(f"Parsed results: {results}")
        return render_template('index.html', team_url=team_url, results=results)
    else:
        return render_template('index.html', team_url='', results=[])


if __name__ == '__main__':
    app.run(debug=True)
