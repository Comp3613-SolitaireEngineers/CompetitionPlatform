from App.database import db

class UserCompetition(db.Model):
    __tablename__ = 'usercompetition'
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    competitor_id =  db.Column(db.String(220), db.ForeignKey('competitor.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def toDict(self):
        res = {
            "id": self.id,
            "comp_id": self.comp_id,
            "competitor_id": self.user_id,
            "rank": self.rank
        } 
        return res