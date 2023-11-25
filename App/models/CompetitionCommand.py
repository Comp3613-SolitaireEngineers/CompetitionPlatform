from datetime import datetime
from App.database import db

class CompetitionCommand(Command):
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

    def execute(self, admin_id, competition_id):
        
        admin = get_admin(admin_id)
        competition = get_competition(competition_id)
        
        if admin:
            if competition:
                admin.add_competition(competition)
            else:
                return ("Unable to add competition")
        else:
            raise PermissionError("Only admins can execute this command.")