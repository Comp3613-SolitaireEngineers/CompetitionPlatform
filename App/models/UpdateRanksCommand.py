from datetime import datetime
from App.database import db
from App.models import Command, Competitor, Rank
from sqlalchemy import desc

class UpdateRanksCommand(Command):
    id = db.Column(db.Integer, primary_key=True)
    # competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, competitor_id):
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
            competitor.rank.ranking = i

        # Commit changes to the database
        db.session.commit()