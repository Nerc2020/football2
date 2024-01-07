from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

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

# Обработчик для главной страницы
@app.route('/', methods=['GET'])
def index():
    hello = 'Добро пожаловать на главную страницу!'
    return render_template('index.html', hello=hello)

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
