from App.database import db, abstractmethod

class LeaderBoardObserver(db.Model):
    
    @abstractmethod
    def update(self):
        pass