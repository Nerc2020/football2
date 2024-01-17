from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class FootballPlayer(Base):
    __tablename__ = 'football_players'
    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    birth_date = Column(String)
    games = Column(Integer)
    goals = Column(Integer)
    nationality = Column(String)
    #team_name = Column(String)

    # Добавляем внешний ключ
    team_name = Column(String, ForeignKey('tournament_table.club'))

    # Определяем отношение к таблице tournament_table
    team = relationship('TournamentTable', back_populates='players')

    def __init__(self, player_name, birth_date, games, goals, nationality, team_name):
        self.player_name = player_name
        self.birth_date = birth_date
        self.games = games
        self.goals = goals
        self.nationality = nationality
        self.team_name = team_name

    def __repr__(self):
        return f"<FootballPlayer(id={self.id}, player_name='{self.player_name}', team_name='{self.team_name}')>"

class TournamentTable(Base):
    __tablename__ = 'tournament_table'
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    club = Column(String)
    matches = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals = Column(String)
    points = Column(Integer)

    # Определяем отношение к таблице football_players
    players = relationship('FootballPlayer', back_populates='team')

    def __init__(self, position, club, matches, wins, draws, losses, goals, points):
        self.position = position
        self.club = club
        self.matches = matches
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals = goals
        self.points = points

    def __repr__(self):
        return f"<TournamentTable(id={self.id}, club='{self.club}', points={self.points})>"

# Путь к базе данных SQLite
db_url = 'sqlite:///football.db'

# Создаем соединение с базой данных SQLite
engine = create_engine(db_url, echo=True)

# Если таблица уже существует, удаляем ее
Base.metadata.reflect(bind=engine)
if FootballPlayer.__tablename__ in Base.metadata.tables:
    FootballPlayer.__table__.drop(engine, checkfirst=True)

if TournamentTable.__tablename__ in Base.metadata.tables:
    TournamentTable.__table__.drop(engine, checkfirst=True)


# Создаем новую таблицу
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()
