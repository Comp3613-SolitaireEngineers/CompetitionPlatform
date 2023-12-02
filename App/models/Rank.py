from App.database import db
from datetime import datetime
from sqlalchemy.sql import func

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'), unique=True)
    ranking = db.Column(db.Integer)
    points = db.Column(db.Integer, default=0, nullable = False)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, competitor_id):
        self.competitor_id = competitor_id

        max_rank = db.session.query(func.max(Rank.ranking)).scalar()
        # If there are existing records, set the new rank to one more than the maximum rank
        # Otherwise, set it to 1 (or any other default initial rank)
        self.ranking = max_rank + 1 if max_rank is not None else 1
        
    def __repr__(self):
        return f'<Rank {self.id}, {self.competitor_id}, Ranking: {self.ranking}, Points {self.points}>'    

    def get_json(self):        
        return{
            'id': self.id,
            'competitor_id': self.competitor_id,
            'ranking': self.ranking,
            'points': self.points,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
  