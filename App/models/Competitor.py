from App.database import db
from .User import User

class Competitor(User):
    __tablename__ = 'competitor'        
    rank = db.relationship('Rank', uselist=False, cascade="all, delete-orphan", lazy=True)
    competitions = db.relationship('Competition', secondary='usercompetition', back_populates='participants')       
    

    def __init__(self, username, password):
        super().__init__(username, password)        

    def __repr__(self):       
        return f"<Competitor {self.id}, {self.username}, {self.rank}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'rank': self.rank.toDict() if self.rank else "",            
        }

    def toDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'rank': self.rank.toDict() if self.rank else "",            
        }
      
