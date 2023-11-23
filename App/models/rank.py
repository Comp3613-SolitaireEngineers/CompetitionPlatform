from App.database import db

class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    ranking = db.Column(db.Integer)
    points = db.Column(db.Integer)
    competitor = db.relationship('Competitor', backref=db.backref('rank', lazy=True))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, competitor_id, ranking):
        self.competitor_id = competitor_id
        self.ranking = ranking

    def __repr__(self):
        return '<Rank %r>' % self.id    

    def get_json(self):        
        return{
            'id': self.id,
            'competitor_id': self.competitor_id,
            'ranking': self.ranking,
            'points': self.points,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def toDict(self):
        res = {
            "id": self.id,
            "competitor_id": self.competitor_id,
            "ranking": self.ranking,
            "points": self.points,
            "competitor": self.competitor.toDict() if self.competitor else "",
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return res