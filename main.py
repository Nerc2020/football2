from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import sqlite3
from model import session, FootballPlayer

app = Flask(__name__)

# Ваша функция для парсинга результатов команды
def parse_team_results(team_url):
    url = f"https://football.kulichki.net/ruschamp/2024/teams/{team_url}.htm"
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

# Новая функция для получения данных из базы данных
def get_tournament_table():
    conn = sqlite3.connect('football.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tournament_table')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_football_players():
    players = session.query(FootballPlayer).all()
    return players

# Обработчик для главной страницы
@app.route('/', methods=['GET'])
def index():
    hello = 'Добро пожаловать на главную страницу!'

    # Получаем данные из базы данных
    tournament_table = get_tournament_table()

    # Получаем данные из базы данных для таблицы FootballPlayer
    football_players = get_football_players()

    return render_template('index.html', hello=hello, tournament_table=tournament_table, football_players=football_players)

# Обработчик для страницы формы
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        team_url = request.form['team_url']
        results = parse_team_results(team_url)
        return render_template('form.html', team_url=team_url, results=results)
    else:
        return render_template('form.html', team_url='', results=[])

# Обработчик для страницы контактов
@app.route('/contacts', methods=['GET'])
def contacts():
    name = 'Sergey Kovalenko'
    email = 'cybermind.space@gmail.com'
    return render_template('contacts.html', name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True)
