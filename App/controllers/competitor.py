from App.models import Competitor, Competition, Rank
from App.database import db
from .rank import create_rank


def create_competitor(username, password):
    competitor = Competitor(username, password)
    try:
        db.session.add(competitor)
        db.session.commit()

        if competitor:
            
    except Exception as e:
        db.session.rollback()
        return False
    return True

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

