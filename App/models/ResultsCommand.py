from datetime import datetime
from App.database import db
from App.models import Command, RankCommand, PointsCommand, UpdateRanksCommand, Competitor, Rank
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
                count = add_results(competition_id, results)
                print("Number added: " + str(count))
                # update points for each competitor
                for competitor in competition.participants:
                    print("Participant added: " + str(competitor.username))
                    updated_points = PointsCommand.PointsCommand(competitor.id)
                    updated_points.execute() #Update points of a competitor
                    
                new_ranks = UpdateRanksCommand.UpdateRanksCommand()
                new_ranks.execute() # Update all ranks
                
                for competitor in Competitor.query.all():                    
                    command = RankCommand(competitor, competitor.rank.ranking)
                    command.execute() #Save new rank, can be used to notify subscribers
            else:
                return ("Unable to add resultss")
        else:
            return ("Unable to add results")
        
        return ("Results added and ranks updated successfully")

    def getRanks(self):
        Ranks = Rank.query.all()
        
        count = 0
        for r in Ranks:
            print(r)
            count += 1
            
        return count
        
        