from App.database import db

class UserCompetition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def toDict(self):
        res = {
            "id": self.id,
            "comp_id": self.comp_id,
            "user_id": self.user_id,
            "rank": self.rank
        } 
        return res