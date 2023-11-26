from App.database import db
from .user import User
from .leaderboard_observer import LeaderboardObserver


class Competitor(User, LeaderBoardObserver):
    __tablename__ = 'competitor'

    rank = db.Column(db.Integer, default=0, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    competitions = db.relationship('Competition', secondary ='competitor_competition', overlaps='competitors', lazy=True)

    def __init__(self, username, password, rank, points):
        super().__init__(username, password)
        self.rank = rank
        self.points = points

    def __repr__(self):       
        return f"<Competitor {self.id}, {self.username} {self.rank} {self.points}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'rank': self.rank,
            'points': self.points
        }
    
    def update(self, rank, points):
        self.rank = rank
        self.points = points

    def subscribe(self, leaderboard):
        leaderboard.register(self)

    
    def unsubscribe(self, leaderboard):
        leaderboard.detach(self)