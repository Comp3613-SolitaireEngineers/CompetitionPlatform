from App.database import db
from .User import User
from .LeaderboardObserver import LeaderboardObserver


class Competitor(User, LeaderboardObserver):
    __tablename__ = 'competitor'

    id = db.Column(db.Integer, db.ForeignKey('leaderboard_observer.id'), nullable=False, primary_key=True)
    points = db.Column(db.Integer, default=0, nullable=False)
    competitions = db.relationship('Competition', secondary='usercompetition', back_populates='participants')
    
    # rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'), nullable=False)
    rank = db.relationship('Rank', back_populates='competitor', uselist=False, cascade="all, delete-orphan", single_parent=True, lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        # self.rank = rank
        self.points = 0

    def __repr__(self):       
        return f"<Competitor {self.id}, {self.username} {self.points}>" #{self.rank}

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            # 'rank': self.rank,
            'points': self.points
        }
    
    def update(self, rank, points):
        self.rank = rank
        self.points = points

    def subscribe(self, leaderboard):
        leaderboard.register(self)

    
    def unsubscribe(self, leaderboard):
        leaderboard.detach(self)