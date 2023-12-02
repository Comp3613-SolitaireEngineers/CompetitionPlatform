from App.models import Competitor, Competition, Rank
from App.database import db
from .rank import create_rank
from sqlalchemy import and_, desc, asc


def create_competitor(uwi_id, username, email ,password, firstname, lastname):
    try:
        competitor = Competitor(uwi_id, username, email, password, firstname, lastname)
        
        db.session.add(competitor)
        db.session.commit()
               
        return competitor   
    except Exception as e:
        print(e)
        db.session.rollback()
    return None


def leaderboard_competitors(page=None):
    competitors_pagination = Competitor.query \
        .join(Rank, Rank.competitor_id == Competitor.id) \
        .order_by(asc(Rank.ranking))
    
    # Extract top 3 competitors
    top_three = competitors_pagination[:3] 

      
    competitors_pagination.offset(3)
    competitors_paginations = competitors_pagination.paginate(page=page, per_page=4)
    

    return {
        'competitors_pagination': competitors_paginations,
        'top_three': top_three,        
    }

def get_competitor_profile(competitor_id):
    competitor = get_competitor_by_id(competitor_id)
    if competitor:
        competitions = []
        for competition in competitor.competitions:
            competition_details = {
                "name": competition.name,
                "location": competition.location,
                "platform": competition.platform,
                "date": competition.date,
               
            }
            competitions.append(competition_details)

        competitor_profile = {"student_id": competitor.uwi_id, 
                              "username": competitor.username, 
                              "name": competitor.firstname + " " + competitor.lastname, 
                              "email": competitor.email,
                              "Rank": competitor.rank.get_json(),
                              "competitions": competitions,
                              "notifications": [notification.toDict() for notification in competitor.notifications] if competitor.notifications else []

                              }
        return competitor_profile
    else:
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

