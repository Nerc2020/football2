# parser.py
from bs4 import BeautifulSoup
import requests
from model import session, FootballPlayer

def parse_and_add_player(url, team_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    player_rows = soup.find_all('tr')

    players_to_add = []

    for row in player_rows:
        if not row.find_all('td'):
            continue

        # Проверим, содержит ли строка заголовки "Вратари", "Защитники", "Полузащитники" или "Нападающие"
        if any(title in row.text for title in ["Вратари", "Защитники", "Полузащитники", "Нападающие"]):
            continue

        columns = row.find_all('td')

        # Добавим проверку на количество столбцов
        if len(columns) < 6:
            continue

        player_link = columns[1].find('a')
        if player_link:
            player_name = player_link.text
        else:
            player_name = columns[1].text

        # Функция для проверки, является ли строка числом
        def parse_numeric(value):
            return int(value.strip()) if value.strip().isdigit() else 0

        player_data = {
            "player_name": player_name,
            "birth_date": columns[2].text,
            "games": parse_numeric(columns[3].text),
            "goals": parse_numeric(columns[4].text),
            "nationality": columns[5].text,
            "team_name": team_name,
        }

        player = FootballPlayer(**player_data)
        players_to_add.append(player)

        print(f"Добавлен игрок: {player_data}")

    session.add_all(players_to_add)
    session.commit()

# Пример использования
parse_and_add_player("https://football.kulichki.net/ruschamp/2024/teams/cska.htm", "ЦСКА")
