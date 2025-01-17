from App.models import Competition,User, Admin
from App.database import db
from App.controllers import get_results_by_competition_id

def create_competition(admin_id,name, location, platform, date):   
    admin = Admin.query.get(admin_id)    
    if admin:
        return admin.create_competition(name, location, platform, date)
    return None

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()
    if not competitions:
        return []
    competitions = [comp.get_json() for comp in competitions]
    return competitions
            
def get_competition_by_id(id):
    if not id:
        return None
    competition = Competition.query.get(id)
    return competition

def get_competition_by_id_json(id):
    competition = get_competition_by_id(id)
    if not competition:
        return []
    competition = competition.get_json()
    return competition


def get_competition_users(comp_id):
    Comp = get_competition_by_id(comp_id)
    

    if Comp:
        compUsers = Comp.participants
        Participants = [User.query.get(part.user_id) for part in compUsers]
        print(Participants)


def get_competition_details(competition_id):
    competition = Competition.query.get(competition_id)
    if competition:
        results = get_results_by_competition_id(competition_id)
        competition_details = {
            "name": competition.name,
            "location": competition.location,
            "platform": competition.platform,
            "date": competition.date.strftime("%d %B, %Y"),
            "results": results        
        }
        return competition_details
    return None
      
