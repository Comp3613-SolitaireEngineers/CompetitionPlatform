from App.database import db
from abc import abstractmethod

class LeaderboardPublisher(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    
    @abstractmethod
    def register(self,observer):
        pass
    
    @abstractmethod
    def detach(self, observer):
        pass
    
    @abstractmethod
    def notify_observer(self):
        pass