from datetime import datetime
from App.database import db
from App.models import Command, RankCommand
from App.controllers import results
from App.controllers import get_admin, get_competition_by_id, add_results

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
    
    def execute(self, admin_id, competition_id, results):
        
        admin = get_admin(admin_id)
        competition = get_competition_by_id(competition_id)
        
        if admin:
            if competition:
                add_results(competition_id, results)
                
                # Create and execute a RankCommand for each competitor
                for competitor in competition.participants:
                    new_rank = calculate_new_rank(competitor)  
                    command = RankCommand(competitor, new_rank)
                    command.execute()
            else:
                return ("Unable to add results")
        else:
            return ("Unable to add results")
