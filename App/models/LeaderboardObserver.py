from App.database import db
from abc import abstractmethod

class LeaderBoardObserver(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    
    @abstractmethod
    def update(self):
        pass