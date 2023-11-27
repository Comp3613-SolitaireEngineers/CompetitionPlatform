from App.models import Competitor, Competition, Rank
from App.database import db
from .rank import create_rank


def create_competitor(username, password):
    try:
        competitor = Competitor(username, password)
        
        db.session.add(competitor)
        db.session.commit()
        
        # Create rank for competitor
        rank = create_rank(competitor.id, -1)  
               
        return competitor   
    except Exception as e:
        print(e)
        db.session.rollback()
    return None

def get_all_competitors():
    competitors = Competitor.query.all()
    return competitors

def get_all_competitors_json():
    competitors = Competitor.query.all()
    return [competitor.get_json() for competitor in competitors]

def get_competitor_by_id(id):
    competitor = Competitor.query.filter_by(id = id).first()
    return competitor

def get_competitor_by_username(username):
    competitor = Competitor.query.filter_by(username = username).first()
    return competitor

def get_competitor_by_username_json(username):
    competitor = Competitor.query.filter_by(username = username).first()
    return competitor.get_json()

