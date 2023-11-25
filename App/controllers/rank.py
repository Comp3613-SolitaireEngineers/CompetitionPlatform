from App.models import Rank, Competitor
from App.database import db

def create_rank(competitor_id, ranking):
    competitor = Competitor.query.filter_by(id = competitor_id).first()
    if competitor is None:
        return False

    newrank = Rank(competitor_id = competitor_id, ranking = ranking)
    try:
        db.session.add(newrank)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False
    return True

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



