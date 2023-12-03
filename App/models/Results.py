from App.database import db
from datetime import datetime

class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'))
    points = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)   
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    competitor = db.relationship('Competitor', uselist=False, lazy=True)
    
    def __init__(self, competition_id, competitor_id, points, rank):
        self.competition_id = competition_id
        self.competitor_id = competitor_id
        self.points = points
        self.rank = rank  
              

    def __repr__(self):
        return f'<Results {self.id}, {self.competition_id}, {self.competitor_id}, {self.rank}, {self.points}>'
    
    def get_json(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'competitor_id': self.competitor_id,
            'rank': self.rank,
            'points': self.points,
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'date_modified': self.date_modified.strftime("%Y-%m-%d %H:%M:%S")
        }