from App.database import db
from datetime import datetime
from sqlalchemy.sql import func
from App.models import Command, Competitor

class RankCommand(Command):
    __tablename__ = 'rank_command'
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'))
    old_rank = db.Column(db.Integer)
    new_rank = db.Column(db.Integer)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, competitor, new_rank):
        self.competitor_id = competitor.id
        if competitor.rank is not None:
            self.old_rank = competitor.rank.ranking
        else:
            self.old_rank = 0
        self.new_rank = new_rank

    def get_json(self):
        return{
            'id': self.id,
            'competition_id': self.competition_id,
            'old_rank': self.old_rank,
            'new_rank': self.new_rank,
            'executed_at' : self.executed_at
        }
        
    def execute(self):
        competitor = Competitor.query.get(self.competitor_id)
        if competitor.rank is not None:
            self.old_rank = competitor.rank.ranking
            competitor.rank.ranking = self.new_rank  # Update the competitor's rank
        else:
            self.old_rank = 0
        db.session.add(competitor)
        db.session.commit()

    def undo(self):
        competitor = Competitor.query.get(self.competitor_id)
        if competitor.rank is not None:
            competitor.rank.ranking = self.old_rank  # Revert the competitor's rank
        else:
            self.old_rank = 0
        db.session.add(competitor)
        db.session.commit()

