from App.models import CompetitionHost
from App.database import db

def create_competition_host(comp_id,host_id):
    try:
        newCompetitionHost = CompetitionHost(comp_id=comp_id, host_id=host_id)
        db.session.add(newCompetitionHost)
        db.session.commit()
        return newCompetitionHost
    except Exception as e:
        print(e)
        db.session.rollback()
    return None

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