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