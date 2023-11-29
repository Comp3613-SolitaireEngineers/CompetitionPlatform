from App.models import Host
from App.database import db

def create_host(id,name,website):
    try:
        newHost = Host(id=id, name=name, website=website)
        db.session.add(newHost)
        db.session.commit()
        return newHost
    except Exception as e:
        print(e)
        db.session.rollback()
    return None
    
def get_host(id):
    return Host.query.filter_by(id).first()

def get_all_hosts_json():
    hosts = Host.query.all()
    if not hosts:
        return []
    hosts = [host.toDict() for host in hosts]
    return hosts