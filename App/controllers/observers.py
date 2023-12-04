from App.models.RankTopObservers import RankTopObservers
from App.database import db

def create_rank_top_observers(name):
    try:
        rank_top_observer = RankTopObservers(name)
        db.session.add(rank_top_observer)
        db.session.commit()
        return rank_top_observer
    except Exception as e:
        print("Error creating rank_top_observers " + str(e))
        
    return None

def get_rank_top_observers_by_name(name):
    return RankTopObservers.query.filter_by(name=name).first()

def get_rank_top_observers_by_id(id):
    return RankTopObservers.query.get(id)

def get_rank_top_observer():
    return RankTopObservers.query.first()