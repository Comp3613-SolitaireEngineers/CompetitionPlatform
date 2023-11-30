from App.database import db
from datetime import datetime
from sqlalchemy.sql import func
from App.models import Competitor

class RankTopObservers(db.Model):
    __tablename__ = 'rank_top_observers'
    id = db.Column(db.Integer, primary_key=True)
    # competitor_id = db.Column(db.String(220), db.ForeignKey('competitor.id'))
    top_subscribers = db.relationship('Competitor', backref='rank_top_observer', lazy=True)

    def __init__(self):
        pass
        # self.competitor_id = competitor.id
        
    def subscribe(self, competitor):
      self.top_subscribers.append(competitor)
      
    def notify_subscribers(self, message):
        for subscriber in self.top_subscribers:
            subscriber.update(message)

    def get_json(self):
        return{
            'id': self.id,
            # 'competitor_id': self.competitor_id,
        }
