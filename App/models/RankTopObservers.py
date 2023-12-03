from App.database import db
from datetime import datetime
from sqlalchemy.sql import func
from App.models import Competitor, Notification

class RankTopObservers(db.Model):
    __tablename__ = 'rank_top_observers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220))
    top_subscribers = db.relationship('Competitor', backref='rank_top_observer', lazy=True)

    def __init__(self, name):
        self.name = name
        
    def subscribe(self, competitor):
        if competitor.rank.ranking <= 20:
            
            #Check if competitor is already subscribed
            ini = False
            for i in self.top_subscribers:
                if i.id == competitor.id:
                    ini = True
            if ini == False:
                self.top_subscribers.append(competitor)
        else:
            print(f"Competitor {competitor.id} does not qualify for top observers")

      
    def unsubscribe(self, competitor):
        self.top_subscribers.remove(competitor)
    
    def notify_subscribers(self, message):
        for subscriber in self.top_subscribers:
            subscriber.update_notifications(message)


    def get_json(self):
        return{
            'id': self.id,
        }
