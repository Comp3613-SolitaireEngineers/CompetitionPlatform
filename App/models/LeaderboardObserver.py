from App.database import db
from abc import abstractmethod

class LeaderboardObserver(db.Model):
    __tablename__ = 'leaderboard_observer'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    
    @abstractmethod
    def update(self):
        pass