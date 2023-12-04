from datetime import datetime
from App.database import db
from App.models import Command
from App.controllers import create_competition

class CompetitionCommand(Command):
    __tablename__ = 'competition_command'
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    executed_at = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self):        
        self.executed_at = datetime.now()

    def get_json(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            "executed_at": self.executed_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def execute(self, admin_id, name, location, platform, date):
        competition  = create_competition(admin_id, name, location, platform, date)
        if competition:
            self.set_competition_id(competition.id)
            return competition
        return None
    
    def set_competition_id(self, competition_id):
        try:
            self.competition_id = competition_id
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print("Error executing competition command: ", e)
            db.session.rollback()
            return None