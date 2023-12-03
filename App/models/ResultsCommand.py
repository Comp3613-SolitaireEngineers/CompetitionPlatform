from datetime import datetime
from App.database import db
from App.models import Command, RankCommand, PointsCommand, UpdateRanksCommand, Competitor, Rank
from App.controllers import *
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
                count = add_results(competition_id, results)
                print("Number added: " + str(count))
                # update points for each competitor
                for competitor in competition.participants:
                    print("Participant added: " + str(competitor.username))
                    updated_points = execute_points_command(admin.id, competitor.id)
                    
                new_ranks = execute_update_ranks_command(admin.id)
                
                for competitor in Competitor.query.all():  
                    pass                  
                    # command = execute_rank_command(admin.id, competitor, competitor.rank.ranking)
            else:
                return ("Unable to add resultss")
        else:
            return ("Unable to add results")
        
        return ("Results added and ranks updated successfully")
