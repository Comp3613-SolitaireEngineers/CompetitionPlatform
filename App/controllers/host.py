from App.models import Host
from App.models import CompetitionHost
from App.database import db
from App.controllers.competition import get_competition_by_id

def create_host(name,website):
    try:
        newHost = Host(name=name, website=website)
        db.session.add(newHost)
        db.session.commit()
        return newHost
    except Exception as e:
        print(e)
        db.session.rollback()
    return None
    
def get_host(id):
    return Host.query.filter_by(id=id).first()

def get_all_hosts_json():
    hosts = Host.query.all()
    if not hosts:
        return []
    hosts = [host.toDict() for host in hosts]
    return hosts

def create_competition_host(competition_id, host_id):
    try:
        host = get_host(host_id)
        if not host:
            return False
        competition = get_competition_by_id(competition_id)
        if not competition:
            return False
        try:
            comp_host = CompetitionHost(comp_id=competition_id, host_id=host_id)
            db.session.add(comp_host)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
    return False