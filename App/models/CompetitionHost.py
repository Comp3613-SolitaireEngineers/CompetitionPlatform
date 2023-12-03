from App.database import db

class CompetitionHost(db.Model):
    __tablename__ = 'competition_host'
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    host_id =  db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)