from App.database import db
from datetime import datetime
from sqlalchemy.sql import desc, asc
from App.models import Competitor, RankCommand, Rank

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
    
    def notify_subscribers(self):
        observers = RankTopObservers.query.first()
        
        # Get all competitors sorted by points in descending order
        competitors = Competitor.query.join(Rank).order_by(asc(Rank.ranking)).all()

        current_top_20 = set(competitors[:20])
        previous_top_20 = set(observers.top_subscribers)
        
        left_top_20 = previous_top_20 - current_top_20
        entered_top_20 = current_top_20 - previous_top_20
        remained_top_20 = current_top_20.intersection(previous_top_20)

        # Unsubscribe the competitors who have left the top 20 and send them a notification
        for competitor in left_top_20:
            observers.unsubscribe(competitor)
            self.update_notifications(competitor, "You have left the top 20. Your rank has changed from {} to {}")

        # Subscribe the competitors who have entered the top 20 and send them a notification
        for competitor in entered_top_20:
            observers.subscribe(competitor)
            self.update_notifications(competitor, "You have entered the top 20. Your rank has changed from {} to {}")

        # Send a notification to the competitors who have remained in the top 20
        for competitor in remained_top_20:
            self.update_notifications(competitor, "You are still in the top 20. Your rank is now {}")

        # Commit the session
        db.session.commit()

        return "Results added and ranks updated successfully"

    #Helper function to update
    def update_notifications(self, competitor, message):
        latest_rank_command = RankCommand.query.filter_by(competitor_id=competitor.id).order_by(RankCommand.executed_at.desc()).first()
        if latest_rank_command:
            if latest_rank_command.old_rank == 0:
                competitor.update_notifications("You are a new competitor and have entered the top 20", "Congragtulations")
            # elif message == "You are still in the top 20. Your rank is now {}" and latest_rank_command.old_rank > latest_rank_command.new_rank:
            #     competitor.update_notifications(message.format(latest_rank_command.old_rank), "Rank Update1")  
            elif message == "You are still in the top 20. Your rank is now {}": 
                competitor.update_notifications(message.format(latest_rank_command.new_rank), "Rank Update2")                 
            else:
                competitor.update_notifications(message.format(latest_rank_command.old_rank, latest_rank_command.new_rank), "Rank Update")
        else:
            competitor.update_notifications("You have entered the top 20", "Congragtulations")


    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
        }
