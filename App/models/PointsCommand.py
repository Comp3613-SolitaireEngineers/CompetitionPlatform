from datetime import datetime
from App.database import db
from App.models import Command, Results, Rank, Competitor
from sqlalchemy import func

class PointsCommand(Command):
    __tablename__ = 'points_command'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, competitor_id):
        # pass
        self.competitor_id = competitor_id

    def get_json(self):
        return{
            'id': self.id,
            'competitor_id': self.competitor_id
        }
        
    def execute(self):
        # Get all competitors

        # Calculate the total points of a competitor
        total_points = db.session.query(func.sum(Results.points)).filter(Results.competitor_id == self.competitor_id).scalar()

        # If total_points is None, set it to 0
        if total_points is None:
            total_points = 0

        # Update the competitor's points in the Rank table
        competitor_rank = Rank.query.filter_by(competitor_id= self.competitor_id).first()
        if competitor_rank:
            competitor_rank.points = total_points

        # Commit changes to the database
        db.session.commit()
