import requests
from bs4 import BeautifulSoup
import sqlite3

# Загрузка HTML-страницы
url = 'https://football.kulichki.net/ruschamp/'
response = requests.get(url)
html = response.text

# Парсинг HTML-страницы
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', {'border': '1'})

# Подключение к базе данных
conn = sqlite3.connect('football.db')
cursor = conn.cursor()

# Очистка таблицы перед вставкой новых данных
cursor.execute('DELETE FROM tournament_table')

# Извлечение данных из таблицы
rows = table.find_all('tr')[1:]  # Пропускаем строчку с заголовком
for row in rows:
    columns = row.find_all('td')
    position = int(columns[0].text.strip())
    club = columns[1].text.strip()
    matches = int(columns[2].text.strip())
    wins = int(columns[3].text.strip())
    draws = int(columns[4].text.strip())
    losses = int(columns[5].text.strip())
    goals = columns[6].text.strip()
    points = int(columns[7].text.strip())

    # Вставка данных в базу данных
    cursor.execute('''
        INSERT INTO tournament_table (position, club, matches, wins, draws, losses, goals, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (position, club, matches, wins, draws, losses, goals, points))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
