from App.models import Rank, Competitor
from App.database import db
from sqlalchemy import desc, asc

def create_rank(competitor_id):
    competitor = Competitor.query.filter_by(id = competitor_id).first()
    if competitor is None:
        return False

    newrank = Rank(competitor_id = competitor_id)
    try:
        db.session.add(newrank)
        db.session.commit()
        return newrank
    except Exception as e:
        print(e)
        db.session.rollback()
    return None

def get_rankings():
    ranks = Rank.query.order_by(asc(Rank.ranking)).all()

    rankings = []
    for rank in ranks:
        competitor = Competitor.query.filter_by(id = rank.competitor_id).first()
        ranking = {
            'competitor_id': rank.competitor_id,
            'username': competitor.username,
            'name': competitor.firstname + ' ' + competitor.lastname,            
            'ranking': rank.ranking,
            'points': rank.points
        }
        rankings.append(ranking)
    return rankings

def update_rank_points(competitor_id, points):
    rank = Rank.query.filter_by(competitor_id = competitor_id).first()
    rank.points = points
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True

def update_rank(competitor_id, ranking):
    rank = Rank.query.filter_by(competitor_id = competitor_id).first()
    rank.ranking = ranking
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True

def get_rank_by_competitor_id(competitor_id):
    rank = Rank.query.filter_by(competitor_id = competitor_id).first()
    return rank

def get_all_ranks():
    ranks = Rank.query.all()
    return ranks


def get_all_ranks_json():
    ranks = Rank.query.all()
    return [rank.get_json() for rank in ranks]



