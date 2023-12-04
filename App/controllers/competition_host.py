from App.models import CompetitionHost
from App.database import db
from App.controllers.host import get_host
from App.controllers.competition import get_competition_by_id

def create_competition_host(competition_id, host_id):
    try:
        host = get_host(host_id)
        if not host:
            return False
        competition = get_competition_by_id(competition_id)
        if not competition:
            return False
    
        comp_host = CompetitionHost(comp_id=competition_id, host_id=host_id)
        db.session.add(comp_host)
        db.session.commit()
       
        
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
    return False

def get_competition_host(id):
    return CompetitionHost.query.filter_by(id).first()

def get_competition_hosts():
    return CompetitionHost.query.all()

def get_all_competition_hosts_json():
    comp_hosts = get_competition_hosts()
    if not comp_hosts:
        return []
    comp_hosts = [comp_host.get_json() for comp_host in comp_hosts]
    return comp_hosts