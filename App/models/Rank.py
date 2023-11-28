from App.database import db
from datetime import datetime

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'))
    ranking = db.Column(db.Integer)
    points = db.Column(db.Integer, default=0)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, competitor_id, ranking):
        self.competitor_id = competitor_id
        self.ranking = ranking

    def __repr__(self):
        return f'<Rank {self.id}, {self.competitor_id}, {self.ranking}, {self.points}>'    

    def get_json(self):        
        return{
            'id': self.id,
            'competitor_id': self.competitor_id,
            'ranking': self.ranking,
            'points': self.points,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def toDict(self):
        res = {
            "id": self.id,
            "competitor_id": self.competitor_id,
            "ranking": self.ranking,
            "points": self.points,           
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return res