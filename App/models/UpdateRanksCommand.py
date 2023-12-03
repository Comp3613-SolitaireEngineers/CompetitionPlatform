from datetime import datetime
from App.database import db
from App.models import Command, Competitor, Rank
from sqlalchemy import desc
from App.controllers import execute_rank_command

class UpdateRanksCommand(Command):
    __tablename__ = 'update_ranks_command'
    id = db.Column(db.Integer, primary_key=True)
    # competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self):
        pass
        # self.competitor_id = competitor_id

    def get_json(self):
        return{
            'id': self.id,
            # 'competitor_id': self.competitor_id
        }
        
    def execute(self):

        # Get all competitors sorted by points in descending order
        competitors = Competitor.query.join(Rank).order_by(desc(Rank.points)).all()

        # Update rank based on position in sorted list
        for i, competitor in enumerate(competitors, 1):
            command = execute_rank_command(competitor.id, competitor.rank.ranking, i)
            competitor.rank.ranking = i

        # Commit changes to the database
        db.session.commit()