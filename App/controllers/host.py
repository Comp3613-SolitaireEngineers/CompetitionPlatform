from App.models import Host
from App.database import db

def create_host(id,name,website):
    host = Host.query.filter_by(id = id).first()
    if host:
        return Host.create_host(name,website)
    return None
    
def get_host(id):
    return Host.query.filter_by(id).first()

def get_all_hosts_json():
    hosts = Host.query.all()
    if not hosts:
        return []
    hosts = [host.get_json() for host in hosts]
    return hosts