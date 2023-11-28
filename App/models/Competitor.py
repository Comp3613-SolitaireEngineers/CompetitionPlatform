from App.database import db
from .User import User

class Competitor(User):
    __tablename__ = 'competitor'        
    rank = db.relationship('Rank', uselist=False, lazy=True)
    competitions = db.relationship('Competition', secondary='usercompetition', back_populates='participants')       
    notifications = db.relationship('Notification', backref='competitor', lazy=True)
    

    def __init__(self, username, password):
        super().__init__(username, password)        

    def __repr__(self):       
        return f"<Competitor {self.id}, {self.username}, {self.rank}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'rank': self.rank.toDict() if self.rank else "",
            'competitions': [comp.get_json() for comp in self.competitions] if self.competitions else [],
            'notifications': [notification.toDict() for notification in self.notifications] if self.notifications else []            
        }

    def toDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'rank': self.rank.toDict() if self.rank else "",
            'competitions': [comp.toDict() for comp in self.competitions] if self.competitions else [],
            'notifications': [notification.toDict() for notification in self.notifications] if self.notifications else []            
        }
      
