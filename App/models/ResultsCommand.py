from datetime import datetime
from App.database import db

class ResultsCommand(Command):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, competition_id):
        self.competition_id = competition_id

    def get_json(self):
        return{
            'id': self.id,
            'competition_id': self.competition_id
        }

    def toDict(self):
        res = {
            "id": self.id,
            "competition_id": self.competition_id,
            "executed_at": self.executed_at,
        } 
        return res